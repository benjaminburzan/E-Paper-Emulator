import json
from PIL import Image, ImageDraw
import io
import os
import threading
import time

currentdir = os.path.dirname(os.path.realpath(__file__))


class _BatchContext:
    """Context manager that suppresses display() calls until the block exits."""

    def __init__(self, epd):
        self._epd = epd

    def __enter__(self):
        self._epd._batching = True
        return self._epd

    def __exit__(self, *exc):
        self._epd._batching = False
        self._epd.display(self._epd.getbuffer(self._epd.image))
        return False


class EPD:
    def __init__(self, config_file="epd2in13", use_tkinter=False,
                 use_color=False, update_interval=2,
                 reverse_orientation=False, port=5000):
        config_path = os.path.join(currentdir, 'config', f'{config_file}.json')
        self.load_config(config_path)

        self.use_color = use_color
        self.image_mode = 'RGB' if self.use_color else '1'

        if reverse_orientation:
            self.width, self.height = self.height, self.width

        self.image = Image.new(
            self.image_mode, (self.width, self.height),
            'white' if self.use_color else 255
        )
        self.use_tkinter = use_tkinter
        self.update_interval = update_interval
        self.port = port
        self._lock = threading.Lock()
        self._batching = False

        if self.use_tkinter:
            self.init_tkinter()
        else:
            self.update_image_bytes()
            self.init_flask()
            self.start_image_update_loop()

        self.draw = ImageDraw.Draw(self.image)

    def load_config(self, config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
            self.width = config.get('width', 122)
            self.height = config.get('height', 250)
            self.color = config.get('color', 'white')
            self.text_color = config.get('text_color', 'black')

    def init_tkinter(self):
        import tkinter as tk
        from PIL import ImageTk
        self.ImageTk = ImageTk
        self.root = tk.Tk()
        self.root.title(
            f"Waveshare {self.width}x{self.height} EPD Emulator"
        )
        self.canvas = tk.Canvas(
            self.root, width=self.width, height=self.height
        )
        self.canvas.pack()
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.image_on_canvas = self.canvas.create_image(
            0, 0, anchor=tk.NW, image=self.tk_image
        )

        self.update_tkinter()

    def update_tkinter(self):
        self.tk_image = self.ImageTk.PhotoImage(self.image)
        self.canvas.itemconfig(self.image_on_canvas, image=self.tk_image)
        self.root.update()

        self.root.after(
            int(self.update_interval * 1000), self.update_tkinter
        )

    def init_flask(self):
        from flask import Flask, render_template_string, send_file
        self.app = Flask(__name__)

        @self.app.route('/')
        def index():
            return render_template_string('''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <style>
                        #screenImage {
                            width: 50%;
                            height: auto;
                            border: 2px solid #333;
                        }
                    </style>
                    <script>
                        function updateImage() {
                            var image = document.getElementById("screenImage");
                            image.src = "screen.png?t=" + new Date().getTime();
                        }

                        setInterval(updateImage, {{ update_ms }});
                    </script>
                </head>
                <body onload="updateImage()">
                    <img id="screenImage" src="screen.png" alt="EPD Emulator">
                </body>
                </html>
            ''', update_ms=int(self.update_interval * 1000))

        @self.app.route('/screen.png')
        def display_image():
            buf = self.image_bytes
            return send_file(
                io.BytesIO(buf.getvalue()),
                mimetype='image/png'
            )

        threading.Thread(target=self.run_flask, daemon=True).start()

    def run_flask(self):
        import webbrowser
        timer = threading.Timer(1.0, webbrowser.open,
                                args=[f"http://127.0.0.1:{self.port}/"])
        timer.daemon = True
        timer.start()
        self.app.run(port=self.port, debug=False, use_reloader=False)

    def update_image_bytes(self):
        buf = io.BytesIO()
        with self._lock:
            self.image.save(buf, format='PNG')
        self.image_bytes = buf

    def start_image_update_loop(self):
        def update_loop():
            while True:
                self.update_image_bytes()
                time.sleep(self.update_interval)

        threading.Thread(target=update_loop, daemon=True).start()

    def init(self):
        print("EPD initialized")

    def Clear(self, color):
        with self._lock:
            self.image = Image.new(
                self.image_mode, (self.width, self.height), color
            )
            self.draw = ImageDraw.Draw(self.image)
        self.display(self.getbuffer(self.image))
        print("Screen cleared")

    def display(self, image_buffer):  # image_buffer accepted for Waveshare API compatibility
        if self.use_tkinter:
            self.tk_image = self.ImageTk.PhotoImage(self.image)
            self.canvas.itemconfig(
                self.image_on_canvas, image=self.tk_image
            )
            self.root.update()
        else:
            self.update_image_bytes()

    def displayPartial(self, image_buffer):
        self.display(image_buffer)

    def get_frame_buffer(self, draw):  # draw accepted for Waveshare API compatibility
        return self.getbuffer(self.image)

    def getbuffer(self, image):
        return image.tobytes()

    def sleep(self):
        print("EPD sleep")

    def Dev_exit(self):
        print("EPD exit")
        if self.use_tkinter:
            self.root.destroy()

    def get_draw_object(self):
        return ImageDraw.Draw(self.image)

    def batch(self):
        """Context manager to batch multiple drawing operations into a single display update.

        Usage:
            with epd.batch():
                epd.draw_rectangle((0, 0, 50, 50), fill=0)
                epd.draw_text((10, 10), "Hello", font=font, fill=0)
            # display() is called once when the block exits
        """
        return _BatchContext(self)

    def draw_text(self, position, text, font, fill):
        with self._lock:
            self.draw.text(position, text, font=font, fill=fill)
        if not self._batching:
            self.display(self.getbuffer(self.image))

    def draw_rectangle(self, xy, outline=None, fill=None):
        with self._lock:
            self.draw.rectangle(xy, outline=outline, fill=fill)
        if not self._batching:
            self.display(self.getbuffer(self.image))

    def draw_line(self, xy, fill=None, width=0):
        with self._lock:
            self.draw.line(xy, fill=fill, width=width)
        if not self._batching:
            self.display(self.getbuffer(self.image))

    def draw_ellipse(self, xy, outline=None, fill=None):
        with self._lock:
            self.draw.ellipse(xy, outline=outline, fill=fill)
        if not self._batching:
            self.display(self.getbuffer(self.image))

    def paste_image(self, image, box=None, mask=None):
        with self._lock:
            self.image.paste(image, box, mask)
        if not self._batching:
            self.display(self.getbuffer(self.image))

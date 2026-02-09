from epaper_emulator.emulator import EPD
from PIL import ImageFont
import time

refreshdelay = 5  # Refresh delay in seconds

# Initialize the emulator
#   config_file: the name of your EPD model
#   use_tkinter: True for Tkinter, False for Flask
#   use_color: True for color, False for monochrome
#   update_interval: refresh delay in seconds
#   reverse_orientation: True to swap width/height

epd = EPD(
    config_file="epd2in13",
    use_tkinter=False,
    use_color=True,
    update_interval=refreshdelay,
    reverse_orientation=False,
)
epd.init()
epd.Clear(255)
width, height = epd.width, epd.height

# Use default font
font = ImageFont.load_default()

toggle = True

while True:
    draw = epd.draw
    draw.rectangle((1, 1, width - 1, height - 1), outline=0)
    draw.line((1, 20, width - 1, 20), fill=0)
    draw.text((10, 5), "EPD Emulator Demo", font=font, fill=0)

    if toggle:
        draw.ellipse((20, 40, width - 20, height - 20), outline=0)
        draw.text((30, height // 2), "Frame A", font=font, fill=0)
    else:
        draw.rectangle((20, 40, width - 20, height - 20), outline=0)
        draw.text((30, height // 2), "Frame B", font=font, fill=0)

    toggle = not toggle

    image_buffer = epd.get_frame_buffer(draw)
    epd.display(image_buffer)

    time.sleep(refreshdelay)

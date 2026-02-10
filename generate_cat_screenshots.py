#!/usr/bin/env python3
"""Generate funny cat screenshots for the E-Paper Emulator README.

Creates two composite images:
  1. The cat displayed inside a browser window (Flask mode)
  2. The cat displayed inside a Tkinter window

Usage:
    python generate_cat_screenshots.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

# --- Colors ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
YELLOW = (255, 220, 0)
DARK_YELLOW = (220, 190, 0)

# Display size (epd5in65)
DISPLAY_W, DISPLAY_H = 600, 448


def draw_funny_cat(draw, W, H):
    """Draw a funny cross-eyed cat with tongue out."""
    cx, cy = W // 2, H // 2 + 20

    # === EARS ===
    draw.polygon(
        [(cx - 130, cy - 80), (cx - 50, cy - 90), (cx - 108, cy - 185)],
        fill=YELLOW, outline=BLACK
    )
    draw.polygon(
        [(cx - 116, cy - 92), (cx - 65, cy - 98), (cx - 105, cy - 162)],
        fill=RED
    )
    draw.polygon(
        [(cx + 130, cy - 80), (cx + 50, cy - 90), (cx + 108, cy - 185)],
        fill=YELLOW, outline=BLACK
    )
    draw.polygon(
        [(cx + 116, cy - 92), (cx + 65, cy - 98), (cx + 105, cy - 162)],
        fill=RED
    )

    # === HEAD ===
    draw.ellipse(
        [(cx - 145, cy - 115), (cx + 145, cy + 135)],
        fill=YELLOW, outline=BLACK, width=3
    )

    # === EYES (cross-eyed) ===
    eye_y = cy - 25
    draw.ellipse(
        [(cx - 90, eye_y - 38), (cx - 18, eye_y + 38)],
        fill=WHITE, outline=BLACK, width=2
    )
    draw.ellipse(
        [(cx - 52, eye_y - 16), (cx - 22, eye_y + 16)], fill=BLACK
    )
    draw.ellipse(
        [(cx - 42, eye_y - 13), (cx - 32, eye_y - 3)], fill=WHITE
    )
    draw.ellipse(
        [(cx + 18, eye_y - 38), (cx + 90, eye_y + 38)],
        fill=WHITE, outline=BLACK, width=2
    )
    draw.ellipse(
        [(cx + 22, eye_y - 16), (cx + 52, eye_y + 16)], fill=BLACK
    )
    draw.ellipse(
        [(cx + 32, eye_y - 13), (cx + 42, eye_y - 3)], fill=WHITE
    )

    # === EYEBROWS ===
    draw.arc(
        [(cx - 88, eye_y - 60), (cx - 20, eye_y - 25)],
        200, 340, fill=BLACK, width=3
    )
    draw.arc(
        [(cx + 20, eye_y - 60), (cx + 88, eye_y - 25)],
        200, 340, fill=BLACK, width=3
    )

    # === BLUSH ===
    draw.ellipse([(cx - 125, cy + 10), (cx - 82, cy + 42)], fill=RED)
    draw.ellipse([(cx + 82, cy + 10), (cx + 125, cy + 42)], fill=RED)

    # === NOSE ===
    nose_y = cy + 30
    draw.polygon(
        [(cx, nose_y - 12), (cx - 14, nose_y + 10), (cx + 14, nose_y + 10)],
        fill=RED, outline=BLACK
    )

    # === MOUTH ===
    draw.arc(
        [(cx - 38, nose_y + 5), (cx + 2, nose_y + 35)],
        0, 180, fill=BLACK, width=2
    )
    draw.arc(
        [(cx - 2, nose_y + 5), (cx + 38, nose_y + 35)],
        0, 180, fill=BLACK, width=2
    )

    # === TONGUE ===
    draw.ellipse(
        [(cx - 12, nose_y + 28), (cx + 12, nose_y + 58)],
        fill=RED, outline=BLACK, width=2
    )
    draw.line(
        [(cx, nose_y + 30), (cx, nose_y + 55)],
        fill=DARK_YELLOW, width=1
    )

    # === WHISKERS ===
    for dy, angle in [(-8, -18), (4, 0), (16, 18)]:
        draw.line(
            [(cx - 55, cy + 28 + dy), (cx - 190, cy + 28 + dy + angle)],
            fill=BLACK, width=2
        )
        draw.line(
            [(cx + 55, cy + 28 + dy), (cx + 190, cy + 28 + dy + angle)],
            fill=BLACK, width=2
        )

    # === WHISKER DOTS ===
    for side in [-1, 1]:
        for row in range(3):
            dot_x = cx + side * 48
            dot_y = cy + 22 + row * 10
            draw.ellipse(
                [(dot_x - 3, dot_y - 3), (dot_x + 3, dot_y + 3)],
                fill=DARK_YELLOW
            )

    # === TEXT ===
    try:
        font_title = ImageFont.truetype(
            "/System/Library/Fonts/Helvetica.ttc", 22
        )
        font_sub = ImageFont.truetype(
            "/System/Library/Fonts/Helvetica.ttc", 16
        )
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    draw.text(
        (W // 2 - 110, 12), "E-Paper Emulator",
        font=font_title, fill=BLACK
    )
    draw.text(
        (W // 2 - 48, H - 28), "Meow! =^..^=",
        font=font_sub, fill=BLACK
    )


def create_cat_image():
    """Create the cat PIL Image."""
    img = Image.new('RGB', (DISPLAY_W, DISPLAY_H), WHITE)
    draw = ImageDraw.Draw(img)
    draw_funny_cat(draw, DISPLAY_W, DISPLAY_H)
    return img


def load_font(size):
    """Load Helvetica or fall back to default."""
    try:
        return ImageFont.truetype(
            "/System/Library/Fonts/Helvetica.ttc", size
        )
    except Exception:
        return ImageFont.load_default()


def create_browser_screenshot(cat_img, output_path):
    """Create a composite image showing the cat inside a browser window."""
    # Browser chrome dimensions
    title_bar_h = 38
    tab_bar_h = 36
    address_bar_h = 34
    chrome_h = title_bar_h + tab_bar_h + address_bar_h
    padding = 20
    body_bg = (246, 246, 246)

    # Scale cat to fit a narrow browser window
    display_scale = 0.88
    scaled_w = int(DISPLAY_W * display_scale)
    scaled_h = int(DISPLAY_H * display_scale)

    browser_w = scaled_w + padding * 2
    browser_h = chrome_h + scaled_h + padding * 2

    img = Image.new('RGB', (browser_w, browser_h), body_bg)
    draw = ImageDraw.Draw(img)

    # --- Title bar (dark gray) ---
    draw.rectangle(
        [(0, 0), (browser_w, title_bar_h)],
        fill=(56, 56, 56)
    )
    # Window control dots
    dot_y = title_bar_h // 2
    for i, color in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        draw.ellipse(
            [(14 + i * 22, dot_y - 6), (26 + i * 22, dot_y + 6)],
            fill=color
        )

    # --- Tab bar ---
    tab_top = title_bar_h
    draw.rectangle(
        [(0, tab_top), (browser_w, tab_top + tab_bar_h)],
        fill=(44, 44, 44)
    )
    # Active tab
    tab_w = 220
    draw.rounded_rectangle(
        [(8, tab_top + 6), (8 + tab_w, tab_top + tab_bar_h)],
        radius=8, fill=(60, 60, 60)
    )
    tab_font = load_font(12)
    draw.text(
        (20, tab_top + 13), "127.0.0.1:5000",
        font=tab_font, fill=(210, 210, 210)
    )

    # --- Address bar ---
    addr_top = tab_top + tab_bar_h
    draw.rectangle(
        [(0, addr_top), (browser_w, addr_top + address_bar_h)],
        fill=(56, 56, 56)
    )
    # URL field
    addr_font = load_font(13)
    bar_left = 50
    bar_right = browser_w - 50
    bar_top_y = addr_top + 6
    bar_bot_y = addr_top + address_bar_h - 6
    draw.rounded_rectangle(
        [(bar_left, bar_top_y), (bar_right, bar_bot_y)],
        radius=10, fill=(36, 36, 36)
    )
    # Lock icon (simple)
    lock_x = bar_left + 12
    lock_y = addr_top + 12
    draw.text(
        (lock_x, lock_y - 2), "\u25CF",
        font=load_font(10), fill=(140, 140, 140)
    )
    draw.text(
        (lock_x + 14, lock_y - 1), "127.0.0.1:5000",
        font=addr_font, fill=(200, 200, 200)
    )

    # --- Body (scaled cat image) ---
    cat_scaled = cat_img.resize(
        (scaled_w, scaled_h), Image.Resampling.LANCZOS
    )
    paste_x = (browser_w - scaled_w) // 2
    paste_y = chrome_h + padding
    img.paste(cat_scaled, (paste_x, paste_y))

    img.save(output_path)
    print(f"Saved browser screenshot: {output_path}")


def create_tkinter_screenshot(cat_img, output_path):
    """Create a composite image showing the cat inside a Tkinter window."""
    # macOS-style Tkinter window chrome
    title_bar_h = 28
    border = 1

    win_w = DISPLAY_W + border * 2
    win_h = DISPLAY_H + title_bar_h + border

    # Shadow + padding
    shadow_offset = 6
    pad = 12
    canvas_w = win_w + pad * 2 + shadow_offset
    canvas_h = win_h + pad * 2 + shadow_offset

    img = Image.new('RGB', (canvas_w, canvas_h), (236, 236, 236))
    draw = ImageDraw.Draw(img)

    ox, oy = pad, pad

    # --- Drop shadow ---
    shadow_color = (180, 180, 180)
    draw.rounded_rectangle(
        [(ox + shadow_offset, oy + shadow_offset),
         (ox + win_w + shadow_offset, oy + win_h + shadow_offset)],
        radius=8, fill=shadow_color
    )

    # --- Window body ---
    draw.rounded_rectangle(
        [(ox, oy), (ox + win_w, oy + win_h)],
        radius=8, fill=(232, 232, 232)
    )

    # --- Title bar ---
    draw.rounded_rectangle(
        [(ox, oy), (ox + win_w, oy + title_bar_h)],
        radius=8, fill=(232, 232, 232)
    )
    # Bottom of title bar is straight
    draw.rectangle(
        [(ox, oy + title_bar_h - 8), (ox + win_w, oy + title_bar_h)],
        fill=(232, 232, 232)
    )
    # Title bar separator
    draw.line(
        [(ox, oy + title_bar_h), (ox + win_w, oy + title_bar_h)],
        fill=(200, 200, 200), width=1
    )

    # Window control dots
    dot_y = oy + title_bar_h // 2
    for i, color in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        draw.ellipse(
            [(ox + 10 + i * 20, dot_y - 5),
             (ox + 20 + i * 20, dot_y + 5)],
            fill=color
        )

    # Title text
    title_font = load_font(13)
    title_text = "Waveshare 600x448 EPD Emulator"
    bbox = draw.textbbox((0, 0), title_text, font=title_font)
    tw = bbox[2] - bbox[0]
    draw.text(
        (ox + (win_w - tw) // 2, oy + 7),
        title_text, font=title_font, fill=(80, 80, 80)
    )

    # --- Cat image (full size) ---
    img.paste(cat_img, (ox + border, oy + title_bar_h))

    img.save(output_path)
    print(f"Saved Tkinter screenshot: {output_path}")


def main():
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "screenshots")
    os.makedirs(out_dir, exist_ok=True)

    cat_img = create_cat_image()

    # Save raw image
    raw_path = os.path.join(out_dir, "cat_raw.png")
    cat_img.save(raw_path)
    print(f"Saved raw image: {raw_path}")

    # Generate browser (Flask) screenshot
    flask_path = os.path.join(out_dir, "screenshot_flask.png")
    create_browser_screenshot(cat_img, flask_path)

    # Generate Tkinter screenshot
    tkinter_path = os.path.join(out_dir, "screenshot_tkinter.png")
    create_tkinter_screenshot(cat_img, tkinter_path)

    print("\nDone! Screenshots saved to screenshots/")


if __name__ == "__main__":
    main()

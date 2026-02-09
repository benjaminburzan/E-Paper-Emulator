"""Tests for the EPD emulator class."""

from unittest.mock import patch
from PIL import Image, ImageFont
from epaper_emulator.emulator import EPD


def make_epd(**kwargs):
    """Create an EPD instance with side-effect-producing methods patched out."""
    defaults = {"use_tkinter": False, "use_color": False}
    defaults.update(kwargs)
    with patch.object(EPD, "init_tkinter"), \
         patch.object(EPD, "init_flask"), \
         patch.object(EPD, "start_image_update_loop"):
        return EPD(**defaults)


class TestEPDInit:
    def test_default_dimensions(self):
        epd = make_epd()
        assert epd.width == 122
        assert epd.height == 250

    def test_custom_config(self):
        epd = make_epd(config_file="epd7in5")
        assert epd.width == 800
        assert epd.height == 480

    def test_reverse_orientation(self):
        epd = make_epd(reverse_orientation=True)
        assert epd.width == 250
        assert epd.height == 122

    def test_monochrome_mode(self):
        epd = make_epd(use_color=False)
        assert epd.image_mode == "1"

    def test_color_mode(self):
        epd = make_epd(use_color=True)
        assert epd.image_mode == "RGB"

    def test_update_interval_stored_in_seconds(self):
        epd = make_epd(update_interval=5)
        assert epd.update_interval == 5


class TestClear:
    def test_clear_with_white(self):
        epd = make_epd(use_color=True)
        epd.Clear("red")
        # After clearing with red, all pixels should be red
        colors = epd.image.getcolors()
        assert colors == [(epd.width * epd.height, (255, 0, 0))]

    def test_clear_monochrome(self):
        epd = make_epd(use_color=False)
        epd.Clear(0)
        colors = epd.image.getcolors()
        # mode '1': 0 = black
        assert colors == [(epd.width * epd.height, 0)]


class TestGetbuffer:
    def test_returns_bytes(self):
        epd = make_epd()
        buf = epd.getbuffer(epd.image)
        assert isinstance(buf, bytes)
        assert len(buf) > 0


class TestDrawingMethods:
    def test_draw_rectangle(self):
        epd = make_epd()
        epd.draw_rectangle((0, 0, 50, 50), outline=0, fill=0)

    def test_draw_line(self):
        epd = make_epd()
        epd.draw_line((0, 0, 50, 50), fill=0, width=1)

    def test_draw_ellipse(self):
        epd = make_epd()
        epd.draw_ellipse((10, 10, 40, 40), outline=0, fill=0)

    def test_draw_text(self):
        epd = make_epd()
        font = ImageFont.load_default()
        epd.draw_text((10, 10), "Hello", font=font, fill=0)


class TestPasteImage:
    def test_paste_image(self):
        epd = make_epd()
        patch_img = Image.new("1", (20, 20), 0)
        epd.paste_image(patch_img, box=(0, 0))

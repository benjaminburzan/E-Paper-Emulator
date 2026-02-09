# EPD Emulator

[![Python 3](https://img.shields.io/badge/Python-3-blue.svg)](https://www.python.org/)
[![Pillow](https://img.shields.io/badge/Pillow-Image%20Processing-yellow.svg)](https://python-pillow.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20Server-lightgrey.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An emulator for Waveshare E-Paper Display (EPD) screens. Develop and test e-paper applications without hardware using either a native GUI window (Tkinter) or a web-based interface (Flask). Supports 19+ display models in both color and monochrome modes.

![image](https://github.com/infinition/EPD-Emulator/assets/37984399/6006d07a-e760-46c8-9ded-731a590179f0)

## Table of Contents

- [Quick Start](#quick-start)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Supported Display Models](#supported-display-models)
- [File Structure](#file-structure)
- [Credits](#credits)
- [License](#license)

---

## Quick Start

> **TL;DR** - Get it running in 3 steps:

1. **Clone this repo** and install dependencies (see [Installation](#installation))
2. **Choose your EPD model** and rendering mode in the demo script
3. **Run it:** `python "waveshare_emulator demo.py"`

---

## Features

- **Dual Rendering Modes**: Tkinter (native GUI window) or Flask (web-based, accessible via browser)
- **Color and Monochrome**: Simulate both color and monochrome e-paper displays
- **19+ EPD Models**: Pre-configured JSON files for a wide range of Waveshare displays
- **Display Orientation**: Normal and reverse orientation support
- **Configurable Refresh Rate**: Adjustable update intervals for the simulation
- **Drawing API**: Text, rectangles, lines, ellipses, and image pasting
- **Drop-in Replacement**: Use the same API as the Waveshare EPD library for seamless development

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/benjaminburzan/EPD-Emulator.git
cd EPD-Emulator
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies:**

| Package | Version | Purpose |
|---------|---------|---------|
| Pillow | >= 10.0.0 | Image processing and drawing |
| Flask | >= 3.0.0 | Web-based display rendering |
| Tkinter | Built-in | Native GUI window rendering |

---

## Usage

### Run the Demo

```bash
python "waveshare_emulator demo.py"
```

The demo script shows how to initialize the emulator, draw shapes and text, and display images.

### Use in Your Own Project

```python
from epd_emulator import epdemulator

# Initialize with your preferred settings
epd = epdemulator.EPD(
    config_file="epd2in13",
    use_tkinter=False,
    use_color=True,
    update_interval=5,
    reverse_orientation=False
)
epd.init()
epd.Clear(255)

# Draw content
draw = epd.draw
draw.text((10, 10), "Hello EPD!", font=font, fill=0)
draw.rectangle((0, 0, epd.width - 1, epd.height - 1), outline=0)

# Display
image_buffer = epd.get_frame_buffer(draw)
epd.display(image_buffer)
```

### Rendering Modes

- **Flask (default)**: Opens `http://127.0.0.1:5000/` in your browser. Set `use_tkinter=False`.
- **Tkinter**: Opens a native desktop window. Set `use_tkinter=True`.

---

## Configuration

All EPD parameters are set when initializing the emulator:

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `config_file` | `str` | EPD model name (matches JSON filename in `config/`) | `epd2in13` |
| `use_tkinter` | `bool` | `True` for native GUI, `False` for Flask web server | `False` |
| `use_color` | `bool` | `True` for RGB color, `False` for monochrome | `False` |
| `update_interval` | `int` | Refresh delay in seconds | `2` |
| `reverse_orientation` | `bool` | Swap width and height | `False` |

### EPD Model Configuration

Each display model is defined by a JSON file in `epd_emulator/config/`:

```json
{
    "name": "epd2in13",
    "width": 122,
    "height": 250,
    "color": "white",
    "text_color": "black"
}
```

---

## Supported Display Models

| Model | Resolution | Size |
|-------|-----------|------|
| `epd1in54` | 200x200 | 1.54" |
| `epd2in7` | 176x264 | 2.7" |
| `epd2in9` | 128x296 | 2.9" |
| `epd2in13` | 122x250 | 2.13" |
| `epd2in13v2` | 122x250 | 2.13" (V2) |
| `epd2in66` | 152x296 | 2.66" |
| `epd3in52` | 240x360 | 3.52" |
| `epd3in7` | 280x480 | 3.7" |
| `epd4in2` | 400x300 | 4.2" |
| `epd4in3` | 800x600 | 4.3" |
| `epd5in65` | 600x448 | 5.65" |
| `epd5in83` | 600x448 | 5.83" |
| `epd6in0` | 800x600 | 6.0" |
| `epd6in2` | 800x480 | 6.2" |
| `epd7in5` | 800x480 | 7.5" |
| `epd9in7` | 1200x825 | 9.7" |
| `epd10in3` | 1872x1404 | 10.3" |
| `epd11in6` | 960x640 | 11.6" |
| `epd12in48` | 1304x984 | 12.48" |

---

## File Structure

```
EPD-Emulator/
├── epd_emulator/               # Main package
│   ├── epdemulator.py          # Core EPD emulator class
│   └── config/                 # EPD model JSON configurations
│       ├── epd1in54.json
│       ├── epd2in13.json
│       ├── ...
│       └── epd12in48.json
├── fonts/                      # Font resources
│   └── Arial.ttf
├── images/                     # Sample images for demo
│   ├── bjorn.bmp
│   └── bjorn1.bmp
├── waveshare_emulator demo.py  # Demo script
├── requirements.txt            # Python dependencies
├── AGENTS.md                   # AI agent guidelines
└── LICENSE                     # MIT License
```

---

## Credits

- Original project: [infinition/EPD-Emulator](https://github.com/infinition/EPD-Emulator)
- E-Paper hardware: [Waveshare](https://www.waveshare.com/)

## License

MIT License - see [LICENSE](LICENSE)

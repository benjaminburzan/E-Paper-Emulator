# Claude Code Project Configuration

## Project Overview

EPD Emulator simulates Waveshare E-Paper Display screens for development and testing. It provides a Python `EPD` class that mimics the Waveshare EPD library API, rendering to either a Tkinter window or a Flask web server.

## Architecture

- **`epd_emulator/epdemulator.py`** - Single-file core. Contains the `EPD` class with all rendering logic (Tkinter + Flask), drawing methods, and configuration loading.
- **`epd_emulator/__init__.py`** - Package entry point. Exports `EPD` and `__version__`.
- **`epd_emulator/config/*.json`** - Display model definitions. Each JSON file has `name`, `width`, `height`, `color`, and `text_color` fields.
- **`waveshare_emulator demo.py`** - Demo script (note the space in filename — always quote it).
- **`tests/`** - Test suite using pytest.

## Key Conventions

- The `EPD` class API mirrors the Waveshare Python library (`init()`, `Clear()`, `display()`, `getbuffer()`, `sleep()`, `Dev_exit()`). Maintain this compatibility.
- Flask mode saves frames as `screen.png` and serves via HTTP with auto-refresh.
- Tkinter mode uses `ImageTk.PhotoImage` with `root.after()` for periodic updates.
- Use Pillow (`PIL`) for all image operations.
- Keep the single-class architecture unless there's a strong reason to split.
- Keep dependencies minimal: Pillow and Flask only. Tkinter is stdlib.

## Quick Reference

| Task | Command |
|------|---------|
| Install (dev) | `pip install -e ".[dev]"` |
| Run demo | `python "waveshare_emulator demo.py"` |
| Run tests | `python -m pytest tests/ -v` |
| Lint | `flake8 epd_emulator/ --max-line-length=120` |
| Add a display model | Create JSON in `epd_emulator/config/`, update README, add test |

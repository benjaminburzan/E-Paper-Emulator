# AGENTS.md

Guidelines for AI agents working on the EPD Emulator codebase.

## Project Overview

EPD Emulator simulates Waveshare E-Paper Display screens for development and testing. It provides a Python `EPD` class that mimics the Waveshare EPD library API, rendering to either a Tkinter window or a Flask web server.

## Architecture

- **`epd_emulator/epdemulator.py`** - Single-file core. Contains the `EPD` class with all rendering logic (Tkinter + Flask), drawing methods, and configuration loading.
- **`epd_emulator/config/*.json`** - Display model definitions. Each JSON file maps a model name to its resolution and default colors.
- **`waveshare_emulator demo.py`** - Demo script showing usage patterns.

## Key Conventions

- The `EPD` class API mirrors the Waveshare Python library (`init()`, `Clear()`, `display()`, `getbuffer()`, `sleep()`, `Dev_exit()`). Maintain this compatibility.
- Configuration files are simple JSON with `name`, `width`, `height`, `color`, and `text_color` fields.
- Flask mode saves frames as `screen.png` in the package directory and serves them via HTTP with auto-refresh.
- Tkinter mode uses `ImageTk.PhotoImage` with `root.after()` for periodic updates.

## Development Guidelines

### Code Style
- Follow existing patterns in `epdemulator.py`.
- Use Pillow (`PIL`) for all image operations.
- Keep the single-class architecture - avoid splitting into multiple modules unless necessary.

### Testing
- No test framework is currently set up. Test changes manually using the demo script.
- When modifying display logic, verify both Tkinter and Flask rendering modes work.

### Adding New EPD Models
1. Create a new JSON file in `epd_emulator/config/` following the existing format.
2. Use the Waveshare datasheet for the correct resolution.
3. Update the supported models table in `README.md`.

### Dependencies
- Keep dependencies minimal: Pillow and Flask only.
- Tkinter is a Python stdlib module - do not add it to `requirements.txt`.

## Common Tasks

| Task | How |
|------|-----|
| Run the demo | `python "waveshare_emulator demo.py"` |
| Add a display model | Create JSON in `epd_emulator/config/`, update README |
| Change default port | Modify `self.app.run(port=5000, ...)` in `epdemulator.py` |

## File Naming

The demo script has a space in its filename (`waveshare_emulator demo.py`). Always quote the path when running it from the command line.

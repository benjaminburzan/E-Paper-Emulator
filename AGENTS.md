# AI Agent Guidelines

Instructions for AI coding agents (Claude Code, Copilot, Cursor, etc.) working on this repository.

## Project Context

E-Paper Emulator simulates Waveshare E-Paper Display screens. It provides a drop-in `EPD` class replacement for the Waveshare Python library, rendering to Tkinter or Flask instead of hardware.

## Architecture

- **Single-file core**: All logic lives in `epaper_emulator/emulator.py` as the `EPD` class. Keep it that way unless there's a strong reason to split.
- **Lazy imports**: `tkinter`, `ImageTk`, `Flask`, and `webbrowser` are imported inside `init_tkinter()` / `init_flask()`, not at module level. This allows testing without Tk installed.
- **Config-driven models**: Display models are JSON files in `epaper_emulator/config/`. Each has `name`, `width`, `height`, `color`, `text_color`.

## Conventions

- **API compatibility**: The `EPD` class mirrors the Waveshare Python EPD library (`init()`, `Clear()`, `display()`, `getbuffer()`, `sleep()`, `Dev_exit()`). Do not rename or remove these methods.
- **Dependencies**: Pillow and Flask only. Tkinter is stdlib. Do not add new dependencies without discussion.
- **Image operations**: Use Pillow (`PIL`) for all image manipulation.
- **Linting**: flake8 with `--max-line-length=120`. CI enforces this.
- **Tests**: pytest. Tests must not require a display server (Tk, Flask side effects are mocked).

## Working with the Code

### Setup

```bash
pip install -e ".[dev]"
```

### Before Committing

```bash
python -m pytest tests/ -v          # All tests must pass
flake8 epaper_emulator/ --max-line-length=120  # No lint errors
```

### Adding a Display Model

1. Create `epaper_emulator/config/<model>.json`
2. Add to the supported displays table in `README.md`
3. The parametrized tests in `tests/test_config.py` will automatically pick it up

### Testing the EPD Class

Tests in `tests/test_epd.py` use `unittest.mock.patch` on `init_tkinter`, `init_flask`, and `start_image_update_loop` to prevent side effects. Follow this pattern for new EPD tests.

## Common Pitfalls

- **Do not import tkinter or Flask at module level** — breaks headless/CI environments.
- **`update_interval` is in seconds** — convert to milliseconds only at call sites (`root.after()`, `setInterval()`).
- **`Clear(color)` must use the `color` parameter** — don't hardcode a default color.
- **No file I/O for display frames** — Flask serves from an in-memory `BytesIO` buffer, not from disk.

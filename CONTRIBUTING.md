# Contributing to E-Paper-Emulator

Thank you for your interest in contributing to E-Paper-Emulator! This guide will help you get started.

## Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/E-Paper-Emulator.git
   cd E-Paper-Emulator
   ```
3. **Install** dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
4. **Create a branch** for your work:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### Making Changes

1. Make your changes in your feature branch
2. Test both rendering modes (Tkinter and Flask) if your change touches display logic
3. Run the test suite:
   ```bash
   python -m pytest tests/
   ```
4. Run the linter:
   ```bash
   flake8 epaper_emulator/
   ```

### Submitting a Pull Request

1. Push your branch to your fork
2. Open a Pull Request against the `main` branch
3. Fill out the PR template completely
4. Ensure CI checks pass

**PR Requirements:**
- Clear description of what changed and why
- One feature or fix per PR
- Tests pass
- No linting errors

## Adding New EPD Models

To add support for a new Waveshare display:

1. Create a JSON config file in `epaper_emulator/config/`:
   ```json
   {
       "name": "epdXinY",
       "width": 200,
       "height": 200,
       "color": "white",
       "text_color": "black"
   }
   ```
2. Use the exact resolution from the [Waveshare datasheet](https://www.waveshare.com/)
3. Name the file to match the model (e.g., `epd2in13.json`)
4. Add the model to the supported displays table in `README.md`
5. Add a test case in `tests/test_config.py`

## Code Style

- Follow existing patterns in `emulator.py`
- Use [Pillow](https://python-pillow.org/) for all image operations
- Keep the single-class architecture unless there's a strong reason to split
- Maintain API compatibility with the Waveshare Python EPD library

## Questions?

Open a [GitHub Discussion](https://github.com/benjaminburzan/E-Paper-Emulator/discussions) for questions that aren't bug reports or feature requests.

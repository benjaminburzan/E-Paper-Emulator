# Claude Code Configuration

See [AGENTS.md](../AGENTS.md) for full project context, architecture, and conventions.

## Quick Reference

| Task | Command |
|------|---------|
| Install (dev) | `pip install -e ".[dev]"` |
| Run demo | `python demo.py` |
| Run tests | `python -m pytest tests/ -v` |
| Lint | `flake8 epaper_emulator/ --max-line-length=120` |
| Add a display model | Create JSON in `epaper_emulator/config/`, update README, add test |

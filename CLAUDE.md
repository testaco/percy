# CLAUDE.md - Percy Project Guidelines

## Commands
- **Python**: First activate venv: `source venv/bin/activate`
- **Run scripts**: `python scripts/<script_name>.py` (see README for options)
- **Testing**: `pytest tests/` or `pytest tests/test_specific.py`
- **Web app**: 
  - Dev: `cd web && npm run dev` (using Turbopack)
  - Build: `cd web && npm run build`
  - Lint: `cd web && npm run lint`
  - Types: `cd web && npm run generate:types`

## Code Style
- Keep files under 250 lines - split larger files by functionality
- Update Changelog.md under [Unreleased] for all changes
- Python: Use type hints and docstrings, follow PEP 8
- Web: TypeScript + Next.js + Tailwind CSS with shadcn/ui components
- Validate JSON data against schemas in /schema folder

## Project Structure
- Follow existing folder structure in README.md
- Add new tests to /tests directory
- Output files go to /outputs directory
- Processed data stored in /data directory

## Error Handling
- Use Python's try/except for graceful failures
- Validate input/output against schemas
- Log errors with context for debugging
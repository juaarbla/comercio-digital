# Repository Guidelines

## Project Structure & Module Organization

This is a Python news pipeline for FP Comercio y Marketing. Root-level scripts implement each stage: `news_aggregator.py`, `clasificador_ra.py`, the `enriquecer_*.py` enrichers, and the `generar_*.py` static-site generators. `run_pipeline.py` orchestrates the daily flow; keep shared paths in `paths.py` and shared HTML helpers in `web_ui_common.py`.

Input sources live in `feeds.json`; curriculum references are in `data/curriculo/`. Runtime JSON, caches, and backups belong in `data/processed/`, `data/cache/`, and `data/backups/`. Generated public content is committed under `docs/` (including `fichas-aula/` and `newsletter/`). Keep operational notes in `_documentacion/`; the MCP server is isolated in `mcp_servers/comercio_digital/`.

## Build, Test, and Development Commands

Create a virtual environment and install dependencies with `python3 -m venv .venv` and `python3 -m pip install -r requirements.txt`. Copy `env.example` to `.env` before using external providers.

- `python3 run_pipeline.py` runs the complete collection-to-site pipeline.
- `python3 generar_web.py` regenerates the main static pages after data changes.
- `python3 generar_fichas_aula.py --max-fichas 10 --limpiar` rebuilds classroom sheets.
- `python3 generar_newsletter.py --periodicidad quincenal --force` creates a newsletter on demand.
- `python3 -m unittest discover -s tests -v` runs the test suite.

## Coding Style & Naming Conventions

Use Python 3, four-space indentation, UTF-8, and Spanish user-facing text. Prefer `snake_case` for functions, variables, JSON fields, and scripts; use descriptive names such as `generar_fichas_aula.py`. Add type hints where they clarify data shapes. Reuse `paths.py` rather than hard-coding locations. No formatter or linter is configured; keep changes PEP 8–readable and validate with `python3 -m py_compile <file>`.

## Testing Guidelines

Place regression tests in `tests/test_<feature>.py` using `unittest`. Test generated content through focused functions or temporary directories; do not alter tracked `data/` or `docs/` as a test side effect. Cover the behavior being fixed, including legacy inputs when applicable.

## Commit & Pull Request Guidelines

Recent commits use short, imperative Spanish subjects, e.g. `Contextualiza las preguntas de aula por RA` or `Actualiza web diaria 2026-08-04`. Keep commits scoped. PRs should explain the affected pipeline stage, list regenerated `docs/` artifacts when relevant, link issues, and include screenshots for visible HTML changes.

## Security & Generated Content

Never commit `.env`, API keys, or Mailgun credentials. Treat `docs/` as generated output: edit source scripts and data first, then regenerate only the affected artifacts.

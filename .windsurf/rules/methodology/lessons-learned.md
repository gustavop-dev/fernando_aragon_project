---
trigger: model_decision
description: Project intelligence and lessons learned. Reference for project-specific patterns, preferences, and key insights discovered during development.
---

# Lessons Learned — FernandoAragonProject

This file captures important patterns, preferences, and project intelligence that help work more effectively with this codebase. Updated as new insights are discovered.

---

## 1. Architecture Patterns

- **Service Layer**: Business logic is in `services/` (e.g., `EmailService`), not in views. Views handle HTTP request/response only; services handle side effects.
- **Function-based Views**: Uses DRF `@api_view` decorators, not class-based ViewSets. Keep this consistent.
- **Static Data over Database**: All 15 program definitions live in TypeScript files (`programs.ts`, `curriculum.ts`), not in the database.
- **Custom Admin Site**: `BaseFeatureAdminSite` replaces default. Models registered on `admin_site` (custom instance), not `admin.site`. Dual admin: `/admin/` (custom) and `/admin-gallery/` (default).
- **Split Settings**: `settings.py` (base) -> `settings_dev.py` -> `settings_prod.py`. Production fails fast if required env vars missing.
- **Feature Flags via Env Vars**: `ENABLE_SILK` controls django-silk. Follow this pattern for optional features.
- **django_attachments**: Was removed in cleanup (2026-03-17) — it was unused code not in `INSTALLED_APPS`.

---

## 2. Code Style & Conventions

- **Email as USERNAME_FIELD**: Custom `User` model uses `email` instead of `username`.
- **Spanish UI Text**: All frontend text and backend email content is in Spanish (hardcoded).
- **Docstrings**: Google-style docstrings with Args/Returns/Raises sections on backend views/services.
- **URL Organization**: Separate files per domain (`urls/contact.py`, `urls/captcha.py`) aggregated in `urls/__init__.py`.
- **Path Aliases**: Vite `@` alias for `src/` directory.
- **Tailwind via Vite Plugin**: TailwindCSS 4 uses `@tailwindcss/vite`, not PostCSS. Custom theme in `styles/theme.css`.
- **Font**: Montserrat primary, set via inline style.
- **Color Palette**: Primary purple `#29235C`, accent gold `#F9B233`, success green `#2FAC66`.

---

## 3. Development Workflow

- **Virtual Environment**: Always activate `backend/venv` before backend commands.
- **Two Terminals**: Backend `:8000`, frontend `:5173`. CORS pre-configured.
- **Fake Data**: `python manage.py create_fake_data` to populate; `delete_fake_data --confirm` to clear.
- **Pre-commit Hook**: Runs `test_quality_gate.py` on staged test files.
- **Huey Immediate Mode**: Dev runs tasks immediately without Redis. Production requires Redis.
- **Custom Coverage Report**: `conftest.py` at backend root generates per-file coverage with function-level analysis.

---

## 4. Testing Insights

- **Backend Test Structure**: Mirrors source (`tests/models/`, `tests/views/`, `tests/services/`, `tests/commands/`, `tests/utils/`). 12 test files, 108 tests, 100% coverage.
- **Frontend Unit Tests**: Vitest + @testing-library/react. 16 test files, 114 tests (components, pages, data, services, routes).
- **Frontend E2E Tests**: Playwright with Chromium. 6 spec files, 17 tests, 6/6 flows covered.
- **Factory Boy**: Available (`factory-boy==3.3.3`). Use factories over manual object creation.
- **Freezegun**: Available (`freezegun==1.5.5`). Never use `datetime.now()` directly in tests.
- **Quality Gate**: Pre-commit and CI enforce standards from `docs/TESTING_QUALITY_STANDARDS.md`.

---

## 5. Deployment and Infrastructure

- **Production DB**: MySQL via env vars. Dev uses SQLite.
- **Systemd Templates**: `scripts/systemd/huey.service` for Huey worker in production.
- **Backup Retention**: 4 backups (~1 month at weekly intervals).
- **Security Headers**: HSTS (1 year), SSL redirect, secure cookies, X-Frame DENY, XSS filter.
- **Required Prod Env Vars**: `DJANGO_SECRET_KEY` and `DJANGO_ALLOWED_HOSTS` mandatory.

---

## 6. System-Specific Knowledge

- **reCAPTCHA Bypass**: When `RECAPTCHA_SECRET_KEY` is empty, verification returns True (dev mode).
- **Two Admin URLs**: `/admin/` (custom sections), `/admin-gallery/` (default Django admin). Intentional.
- **Custom Coverage Hook**: `conftest.py` suppresses pytest-cov's default terminal summary and replaces it with a richer custom report.

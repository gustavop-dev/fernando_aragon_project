# Active Context — Corporación Fernando de Aragón

_Last updated: 2026-03-17 (post-test-infrastructure)_

---

## 1. Current State

The project is a **functional lead generation website** for a Colombian educational institution. Both backend and frontend are feature-complete for the initial scope:

- **Frontend**: 3 pages (Home, English, ProgramPage) covering all 15 programs with lead forms, WhatsApp CTA, responsive navigation, and animated UI
- **Backend**: Contact form API with email notifications, reCAPTCHA integration, custom User model, Django Admin, and scheduled background tasks (backups, profiling)
- **Infrastructure**: Huey + Redis task queue, django-dbbackup, django-silk profiling (optional), production settings with security hardening

The site is in a **production-ready state** for its core purpose (lead capture), with the main gaps being testing and SEO.

---

## 2. Recent Focus Areas

- **Test infrastructure setup (2026-03-17)** — Comprehensive test quality and coverage improvement:
  - Backend: Added `test_email_service.py` (6 tests) covering `EmailService` — `base_feature_app` now at **100% coverage** (75 tests)
  - Frontend unit: Set up Vitest with `@testing-library/react`, created 4 test files (22 tests) covering `api.ts`, `programs.ts`, `curriculum.ts`, `routes.ts`
  - Frontend E2E: Set up Playwright with Chromium, created 3 E2E test files (9 tests) covering home page, contact form, program navigation
  - Quality gate: Fixed 4 errors (forbidden tokens in test names, useless assertions) — **quality gate now passes** (0 errors, 4 warnings)
- **General cleanup (2026-03-17)** — Backend: removed `django_attachments/` (unused app), `utils/auth_utils.py` (empty), `easy-thumbnails` dep, cleaned settings.py/pytest.ini. Frontend: removed `imports/pasted_text/` (14 raw source files), 7 unused npm deps.
- Memory Bank initialization — created methodology documentation files with full codebase deep-dive

---

## 3. Active Decisions & Considerations

| Decision | Status | Notes |
|----------|--------|-------|
| Frontend testing framework (Vitest) | ✅ Done | `vitest.config.ts`, setup file, 4 test files, 22 tests passing |
| E2E testing with Playwright | ✅ Done | `playwright.config.ts`, 3 E2E files, 9 tests passing |
| SEO strategy (meta tags vs SSR/SSG) | Pending | Current SPA model limits SEO; needs evaluation |
| django_attachments | Removed | Deleted in cleanup (2026-03-17) |
| User authentication for public site | Deferred | Not needed for lead generation scope |

---

## 4. Development Environment Summary

| Component | URL | Status |
|-----------|-----|--------|
| Backend (Django) | `http://localhost:8000` | ✅ Ready |
| Frontend (Vite) | `http://localhost:5173` | ✅ Ready |
| Django Admin | `http://localhost:8000/admin` | ✅ Ready |
| API Health Check | `http://localhost:8000/api/health/` | ✅ Ready |
| Redis (Huey) | `redis://localhost:6379/1` | Required for production tasks |

### Key Commands

```bash
# Backend
source backend/venv/bin/activate
python manage.py runserver

# Frontend
cd frontend && npm run dev

# Backend tests
cd backend && pytest -v
cd backend && pytest --cov

# Frontend unit tests
cd frontend && npm test
cd frontend && npm run test:coverage

# Frontend E2E tests
cd frontend && npm run test:e2e

# Fake data
python manage.py create_fake_data
python manage.py delete_fake_data --confirm
```

---

## 5. Next Steps

### Immediate (High Priority)

1. ~~**Set up frontend testing**~~ ✅ Done — Vitest configured, 22 tests passing
2. ~~**Set up E2E testing**~~ ✅ Done — Playwright configured, 9 tests passing (3 flows)
3. ~~**Add missing backend tests**~~ ✅ Done — `EmailService` tested, 100% coverage

### Short-term (Medium Priority)

4. **SEO improvements** — Add `<title>` and `<meta>` tags per program page via React Helmet or similar
5. **Structured data** — Add JSON-LD schema for educational programs
6. **Frontend input validation** — Add Zod schemas for form data before API submission

### Longer-term (Low Priority)

7. **Evaluate SSR/SSG** — Consider Next.js migration or prerendering for better SEO
8. **i18n** — Only if English version of the site is needed

---

## 6. File Counts (Verified 2026-03-17)

| Category | Count |
|----------|-------|
| Backend model files | 1 (User) |
| Backend view files | 2 (contact, captcha) |
| Backend serializer files | 1 (ContactForm) |
| Backend URL files | 2 (contact, captcha) |
| Backend service files | 1 (EmailService) |
| Backend test files | 11 |
| Backend management commands | 4 (create_fake_data, create_users, delete_fake_data, silk_garbage_collect) |
| Frontend pages | 3 (Home, English, ProgramPage) |
| Frontend custom components | 8 (7 root + 1 in figma/) |
| Frontend UI primitives (shadcn) | 46 |
| Frontend data files | 2 (programs, curriculum) |
| Frontend service files | 1 (api.ts) |
| Frontend unit test files | 4 (api, programs, curriculum, routes) |
| Frontend E2E test files | 3 (home, contact-form, program-page) |
| Programs defined | 15 |
| Frontend routes | 3 (/, /ingles, /:slug) |
| API endpoints | 4 (health, contact submit, captcha site-key, captcha verify) |

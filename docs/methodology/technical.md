# Technical Documentation — Corporación Fernando de Aragón

## 1. Technology Stack

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.12+ | Programming language |
| Django | 6.0.2 | Web framework |
| Django REST Framework | 3.16.1 | REST API toolkit |
| django-cors-headers | 4.9.0 | CORS middleware |
| python-dotenv | 1.2.1 | Environment variable management |
| requests | 2.32.5 | HTTP client (reCAPTCHA verification) |
| Pillow | 12.1.1 | Image processing |
| django-dbbackup | 4.0+ | Database & media backup automation |
| django-silk | 5.0+ | Query profiling (optional, behind feature flag) |
| django-cleanup | 9.0.0 | Auto-delete orphaned files |
| Huey | 2.5+ | Lightweight task queue |
| Redis | 4.0+ | Message broker for Huey |
| Faker | 40.5.1 | Fake data generation |
| factory-boy | 3.3.3 | Test factories |
| freezegun | 1.5.5 | Time mocking for tests |
| pytest | 9.0.2 | Testing framework |
| pytest-django | 4.12.0 | Django integration for pytest |
| pytest-cov | 7.0.0 | Coverage plugin |
| coverage | 7.13.4 | Coverage measurement |
| Ruff | 0.15.2 | Python linter/formatter |

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| Vite | 6.3.5 | Build tool and dev server |
| React | 18.3.1 | UI library |
| TypeScript | 5.5+ | Type-safe JavaScript |
| React Router | 7.13.0 | Client-side routing |
| TailwindCSS | 4.1.12 | CSS framework (via `@tailwindcss/vite`) |
| MUI (Material UI) | 7.3.5 | Component library |
| Radix UI / shadcn | Various | Accessible UI primitives (46 components) |
| Lucide React | 0.487.0 | Icon library |
| Motion (Framer) | 12.23.24 | Animations |
| Embla Carousel | 8.6.0 | Carousel component |
| React Hook Form | 7.55.0 | Form handling |
| Recharts | 2.15.2 | Charts/data visualization |
| Sonner | 2.0.3 | Toast notifications |
| date-fns | 3.6.0 | Date utilities |
| vaul | 1.1.2 | Drawer component |
| cmdk | 1.1.1 | Command palette |
| clsx + tailwind-merge | 2.1.1 / 3.2.0 | Class name utilities |
| class-variance-authority | 0.7.1 | Component variant management |

### Quality & Tooling

| Tool | Purpose |
|------|---------|
| pre-commit | Git hooks (test quality gate on staged test files) |
| `scripts/test_quality_gate.py` | Custom test quality gate CLI |
| `scripts/run-tests-all-suites.py` | Global test runner |
| `scripts/quality/` | Quality gate analyzer modules (backend, frontend unit, E2E, linting, patterns) |
| GitHub Actions | CI workflow (`test-quality-gate.yml`) |

---

## 2. Development Setup

### Prerequisites

- Python 3.12+
- Node.js 20+, npm
- Redis (for Huey task queue)
- Git

### Backend

```bash
python3 -m venv backend/venv
source backend/venv/bin/activate
pip install -r backend/requirements.txt
cp backend/.env.example backend/.env
# Edit backend/.env
python manage.py migrate --settings=base_feature_project.settings
python manage.py createsuperuser --settings=base_feature_project.settings
python manage.py runserver
```

- Backend runs on `http://localhost:8000`
- Django Admin: `http://localhost:8000/admin`
- Health check: `http://localhost:8000/api/health/`

### Frontend

```bash
cd frontend
npm install
cp .env.example .env.local
# Set VITE_API_URL=http://localhost:8000/api
npm run dev
```

- Frontend runs on `http://localhost:5173`

---

## 3. Environment Configuration

### Backend (`backend/.env`)

| Variable | Default | Description |
|----------|---------|-------------|
| `DJANGO_ENV` | `development` | Environment (development/production) |
| `DJANGO_SECRET_KEY` | `change-me` | Django secret key |
| `DJANGO_DEBUG` | `true` | Debug mode |
| `DJANGO_ALLOWED_HOSTS` | _(empty)_ | Comma-separated allowed hosts |
| `DJANGO_DB_ENGINE` | `sqlite3` | Database engine |
| `DJANGO_DB_NAME` | `db.sqlite3` | Database name |
| `DB_USER` / `DB_PASSWORD` / `DB_HOST` / `DB_PORT` | — | MySQL credentials (production) |
| `DJANGO_CORS_ALLOWED_ORIGINS` | `localhost:5173,localhost:3000` | CORS origins |
| `DJANGO_EMAIL_HOST` | `smtp.gmail.com` | SMTP host |
| `DJANGO_EMAIL_HOST_USER` / `PASSWORD` | _(empty)_ | SMTP credentials |
| `CONTACT_NOTIFICATION_EMAIL` | `DEFAULT_FROM_EMAIL` | Where lead notifications go |
| `REDIS_URL` | `redis://localhost:6379/1` | Redis for Huey |
| `ENABLE_SILK` | `false` | Enable query profiling |
| `RECAPTCHA_SITE_KEY` / `SECRET_KEY` | _(empty)_ | reCAPTCHA keys (bypassed when empty) |
| `BACKUP_STORAGE_PATH` | `/var/backups/base_feature_project` | Backup storage directory |

### Frontend (`frontend/.env.local`)

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_URL` | `http://localhost:8000/api` | Backend API base URL |

---

## 4. Key Technical Decisions

1. **Static Program Data** — All program information (15 programs) is defined in TypeScript data files (`programs.ts`, `curriculum.ts`), not stored in the database. This eliminates admin UI complexity and keeps the frontend self-contained.

2. **Email-based User Model** — Custom `User` model with `email` as `USERNAME_FIELD` instead of username. Two roles: `customer` and `admin`.

3. **Function-based Views** — Backend uses DRF function-based views with `@api_view` decorators rather than class-based ViewSets, keeping the API simple.

4. **Service Layer Pattern** — Business logic (email sending) is encapsulated in `services/email_service.py`, not in views.

5. **No Authentication Required** — The public website doesn't require user login. All API endpoints use `AllowAny` permission.

6. **Huey for Background Tasks** — Lightweight alternative to Celery. Runs in immediate mode during development (no Redis required), uses Redis in production.

7. **Split Settings** — `settings.py` (base) → `settings_dev.py` (dev overrides) → `settings_prod.py` (production hardening with required env vars, security headers).

8. **TailwindCSS 4 via Vite Plugin** — Uses `@tailwindcss/vite` instead of PostCSS plugin, with custom theme in `theme.css`.

9. **shadcn/ui Components** — 46 Radix-based UI primitive components in `components/ui/`, providing accessible, composable building blocks.

---

## 5. Design Patterns

| Pattern | Where | Description |
|---------|-------|-------------|
| Service Layer | `services/email_service.py` | Business logic separated from views |
| Custom Manager | `models/user.py` (`UserManager`) | Encapsulated user creation logic |
| Static Data Files | `data/programs.ts`, `data/curriculum.ts` | Program content as typed constants |
| Route-per-Program | `routes.ts` with `/:slug` | Dynamic routing for 15 programs |
| Layout Pattern | `Layout.tsx` with `<Outlet />` | Shared Navbar/Footer/WhatsApp across all pages |
| Component Composition | shadcn/ui primitives | Small, composable UI components via Radix |
| Environment Abstraction | `settings.py` + `.env` | All secrets/config via environment variables |
| Feature Flags | `ENABLE_SILK` | Optional features behind env var flags |
| Scheduled Tasks | `tasks.py` via Huey `@periodic_task` | Cron-like scheduling for backups and maintenance |

---

## 6. Testing Strategy

### Backend (pytest)

- **Framework**: pytest + pytest-django + factory-boy + freezegun
- **Config**: `backend/pytest.ini`
- **Root conftest**: `backend/conftest.py` — custom coverage report with per-file breakdown, function coverage, and top-10 focus list
- **App conftest**: `backend/base_feature_app/tests/conftest.py` — shared fixtures

**Test file inventory (12 test files, 108 tests, 100% coverage):**

| Directory | Files | Tests |
|-----------|-------|-------|
| `tests/models/` | `test_user_model.py` | User model tests |
| `tests/views/` | `test_captcha_views.py`, `test_contact_views.py` | View/endpoint tests |
| `tests/services/` | `test_email_service.py` | EmailService tests |
| `tests/commands/` | `test_silk_garbage_collect.py`, `test_tasks.py` | Management command tests |
| `tests/utils/` | `test_admin.py`, `test_forms.py`, `test_fixtures_and_helpers.py`, `test_pytest_summary_total.py`, `test_run_tests_suites.py`, `test_settings.py`, `test_urls.py` | Admin, forms, URLs, quality tooling tests |

### Frontend Unit (Vitest)

- **Framework**: Vitest + @testing-library/react + jsdom
- **Config**: `frontend/vitest.config.ts`
- **114 tests** across 16 test files (components, pages, data, services, routes)

### Frontend E2E (Playwright)

- **Framework**: Playwright with Chromium
- **Config**: `frontend/playwright.config.ts`
- **17 tests** across 6 E2E spec files, 6/6 flows covered

### Quality Gate

- Pre-commit hook runs `test_quality_gate.py` on staged test files
- GitHub Actions workflow: `.github/workflows/test-quality-gate.yml`
- Enforces naming, assertions, isolation, determinism standards from `docs/TESTING_QUALITY_STANDARDS.md`

---

## 7. CI/CD

- **GitHub Actions**: `test-quality-gate.yml` — runs on test file changes
- **Pre-commit**: Local quality gate hook for staged test files
- **Deployment**: Not automated via CI (manual deployment)

---

## 8. Project Structure

```
fernando_aragon_project/
├── backend/                              # Django Backend
│   ├── base_feature_app/                # Main Django app
│   │   ├── models/                      # 1 model file (User)
│   │   ├── serializers/                 # 1 serializer (ContactForm)
│   │   ├── views/                       # 2 view files (contact, captcha)
│   │   ├── urls/                        # 2 URL files (contact, captcha)
│   │   ├── services/                    # 1 service (EmailService)
│   │   ├── forms/                       # 1 form file (User admin forms)
│   │   ├── tests/                       # 10 test files across 5 directories
│   │   ├── management/commands/         # 3 commands (create_fake_data, create_users, delete_fake_data)
│   │   └── admin.py                     # Custom admin site + User admin
│   ├── base_feature_project/            # Django project config
│   │   ├── settings.py                  # Base settings
│   │   ├── settings_dev.py              # Development overrides
│   │   ├── settings_prod.py             # Production hardening
│   │   ├── urls.py                      # Root URLs
│   │   ├── tasks.py                     # Huey scheduled tasks (3 tasks)
│   │   ├── management/commands/         # 1 command (silk_garbage_collect)
│   │   └── wsgi.py / asgi.py           # Server entry points
│   ├── conftest.py                      # Root pytest conftest (custom coverage report)
│   ├── pytest.ini                       # Pytest configuration
│   ├── requirements.txt                 # 25 Python dependencies
│   └── .env.example                     # Environment template
│
├── frontend/                             # Vite + React SPA
│   ├── src/
│   │   ├── app/
│   │   │   ├── pages/                   # 3 page components (Home, English, ProgramPage)
│   │   │   ├── components/              # 8 custom components + 46 shadcn/ui primitives
│   │   │   ├── data/                    # 2 data files (programs, curriculum)
│   │   │   ├── services/               # 1 API client (api.ts)
│   │   │   ├── routes.ts               # React Router config (3 routes)
│   │   │   └── App.tsx                  # Root component
│   │   ├── assets/                      # 2 static assets
│   │   ├── styles/                      # 4 CSS files (index, tailwind, theme, fonts)
│   │   └── main.tsx                     # Entry point
│   ├── package.json                     # 63 npm packages (50 deps + 13 devDeps)
│   ├── vite.config.ts                   # Vite + React + Tailwind config
│   ├── tsconfig.json                    # TypeScript config
│   └── .env.example                     # VITE_API_URL
│
├── scripts/                              # Quality & tooling
│   ├── run-tests-all-suites.py          # Global test runner
│   ├── test_quality_gate.py             # Quality gate CLI
│   ├── quality/                         # 7 analyzer modules
│   └── systemd/                         # Huey service template + README
│
├── docs/                                 # Development standards
│   ├── methodology/                     # Memory Bank files
│   ├── literature/                      # Research references
│   ├── DJANGO_REACT_ARCHITECTURE_STANDARD.md
│   ├── TESTING_QUALITY_STANDARDS.md
│   ├── BACKEND_AND_FRONTEND_COVERAGE_REPORT_STANDARD.md
│   ├── E2E_FLOW_COVERAGE_REPORT_STANDARD.md
│   ├── TEST_QUALITY_GATE_REFERENCE.md
│   ├── GLOBAL_RULES_GUIDELINES.md
│   └── USER_FLOW_MAP.md
│
├── tasks/                                # Task tracking
│   └── rfc/                             # RFCs for individual tasks
│
├── .windsurf/                            # IDE rules & workflows
│   ├── rules/                           # 13 rule files + methodology/ (8 files)
│   └── workflows/                       # 8 workflow files
│
├── .github/workflows/                    # CI (test-quality-gate.yml)
├── .pre-commit-config.yaml              # Pre-commit hooks
├── .gitignore
└── README.md
```

---

## 9. Constraints

- **No CMS**: Program content changes require code edits to `programs.ts` / `curriculum.ts`
- **SQLite for dev**: Production requires MySQL (configured via env vars)
- **Single Django app**: All business logic in `base_feature_app`
- **Spanish-only**: No i18n framework configured; UI text is hardcoded in Spanish
- **No SSR/SSG**: Pure SPA — no server-side rendering for SEO (relies on slug-based routing)

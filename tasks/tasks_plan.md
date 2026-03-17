# Tasks Plan — Corporación Fernando de Aragón

## 1. Feature Status

| # | Feature | Status | Notes |
|---|---------|--------|-------|
| 1 | Home page (hero, stats, programs, testimonials, lead form) | ✅ Done | `Home.tsx` (28,467 bytes) |
| 2 | English program landing page | ✅ Done | `English.tsx` (32,158 bytes) |
| 3 | Dynamic program pages (15 programs) | ✅ Done | `ProgramPage.tsx` (27,531 bytes) via `/:slug` route |
| 4 | Lead capture form (LeadForm component) | ✅ Done | Light/dark variants, program pre-selection |
| 5 | Contact form API endpoint | ✅ Done | `POST /api/contact/submit/` with serializer validation |
| 6 | Email notification service | ✅ Done | `EmailService.send_contact_notification()` |
| 7 | Google reCAPTCHA integration | ✅ Done | Backend verification + site key endpoint |
| 8 | WhatsApp floating button | ✅ Done | `WhatsAppButton.tsx` on all pages |
| 9 | Responsive Navbar with programs dropdown | ✅ Done | `Navbar.tsx` (11,324 bytes) |
| 10 | Footer | ✅ Done | `Footer.tsx` (5,059 bytes) |
| 11 | Animated counters (scroll-triggered) | ✅ Done | `AnimatedCounter.tsx` |
| 12 | Curriculum accordion per program | ✅ Done | `CurriculumSection.tsx` |
| 13 | Custom User model (email-based) | ✅ Done | `models/user.py` with roles |
| 14 | Custom Django Admin | ✅ Done | `BaseFeatureAdminSite` with sections |
| 15 | Fake data management commands | ✅ Done | `create_fake_data`, `create_users`, `delete_fake_data` |
| 16 | Automated backups (Huey) | ✅ Done | Weekly DB + media backup |
| 17 | Silk query profiling (optional) | ✅ Done | Behind `ENABLE_SILK` flag |
| 18 | Silk garbage collection task | ✅ Done | Daily, 7-day retention |
| 19 | Weekly slow query report | ✅ Done | Generates log file report |
| 20 | Production settings hardening | ✅ Done | `settings_prod.py` with required env vars |
| 21 | Pre-commit quality gate hook | ✅ Done | Runs on staged test files |
| 22 | GitHub Actions CI | ✅ Done | `test-quality-gate.yml` |
| 23 | shadcn/ui component library | ✅ Done | 46 Radix-based UI primitives + 1 figma utility |
| 24 | Program data files (TypeScript) | ✅ Done | 15 programs in `programs.ts`, curriculum in `curriculum.ts` |
| 25 | Backend test suite | ✅ Done | 11 test files, 75 tests, 100% coverage on base_feature_app |
| 26 | Custom coverage report (conftest) | ✅ Done | Per-file breakdown with function coverage |
| 27 | Frontend unit test suite (Vitest) | ✅ Done | 4 test files, 22 tests (api, programs, curriculum, routes) |
| 28 | E2E test suite (Playwright) | ✅ Done | 3 test files, 9 tests (home, contact-form, program-page) |
| 29 | SEO optimization | ❌ Not started | No meta tags, SSR/SSG, or structured data |
| 30 | ~~django_attachments integration~~ | Removed | App deleted in cleanup (2026-03-17) |

---

## 2. Known Issues & Tech Debt

| # | Issue | Severity | Description |
|---|-------|----------|-------------|
| 1 | ~~No frontend tests~~ | ~~High~~ | ✅ Resolved: Vitest + 22 tests |
| 2 | ~~No E2E tests~~ | ~~High~~ | ✅ Resolved: Playwright + 9 tests |
| 3 | No SEO meta tags | Medium | SPA has no `<meta>` tags, Open Graph, or structured data |
| 4 | No SSR/SSG | Medium | Pure SPA — search engines may not index program pages properly |
| 5 | ~~`auth_utils.py` is empty~~ | ~~Low~~ | Removed in cleanup (2026-03-17) |
| 6 | ~~Empty serializer/service test dirs~~ | ~~Low~~ | ✅ Resolved: `tests/services/test_email_service.py` added |
| 7 | ~~django_attachments inactive~~ | ~~Low~~ | Removed in cleanup (2026-03-17) |
| 8 | AllowAny on all endpoints | Medium | No authenticated endpoints; JWT installed but unused |
| 9 | No input sanitization on frontend | Low | LeadForm relies solely on backend validation |
| 10 | Hardcoded Spanish text | Low | No i18n framework; all UI text in Spanish |

---

## 3. Testing Status

### Backend (75 tests, 100% coverage)

| Category | Test Files | Status |
|----------|-----------|--------|
| Models | 1 (`test_user_model.py`) | ✅ Has tests |
| Views | 2 (`test_captcha_views.py`, `test_contact_views.py`) | ✅ Has tests |
| Services | 1 (`test_email_service.py`) | ✅ Has tests |
| Commands | 2 (`test_silk_garbage_collect.py`, `test_tasks.py`) | ✅ Has tests |
| Utils/Admin | 5 (`test_admin.py`, `test_forms.py`, `test_pytest_summary_total.py`, `test_run_tests_suites.py`, `test_urls.py`) | ✅ Has tests |
| **Total** | **11 test files, 75 tests** | **100% coverage** |

### Frontend Unit (22 tests)

| Category | Test Files | Status |
|----------|-----------|--------|
| Services | 1 (`api.test.ts`) | ✅ 6 tests |
| Data | 2 (`programs.test.ts`, `curriculum.test.ts`) | ✅ 13 tests |
| Routes | 1 (`routes.test.ts`) | ✅ 3 tests |

### Frontend E2E (9 tests)

| Category | Test Files | Status |
|----------|-----------|--------|
| Home page | 1 (`home-page-load.spec.ts`) | ✅ 3 tests |
| Contact form | 1 (`contact-form-submit.spec.ts`) | ✅ 3 tests |
| Program navigation | 1 (`program-page-navigation.spec.ts`) | ✅ 3 tests |

---

## 4. Documentation Status

| Document | Location | Status |
|----------|----------|--------|
| README.md | `/README.md` | ✅ Comprehensive |
| Architecture Standard | `docs/DJANGO_REACT_ARCHITECTURE_STANDARD.md` | ✅ Done |
| Testing Quality Standards | `docs/TESTING_QUALITY_STANDARDS.md` | ✅ Done |
| Coverage Report Standard | `docs/BACKEND_AND_FRONTEND_COVERAGE_REPORT_STANDARD.md` | ✅ Done |
| E2E Flow Coverage Standard | `docs/E2E_FLOW_COVERAGE_REPORT_STANDARD.md` | ✅ Done |
| Quality Gate Reference | `docs/TEST_QUALITY_GATE_REFERENCE.md` | ✅ Done |
| Global Rules | `docs/GLOBAL_RULES_GUIDELINES.md` | ✅ Done |
| User Flow Map | `docs/USER_FLOW_MAP.md` | ✅ Done |
| PRD | `docs/methodology/product_requirement_docs.md` | ✅ Done |
| Technical Docs | `docs/methodology/technical.md` | ✅ Done |
| Architecture | `docs/methodology/architecture.md` | ✅ Done |
| Active Context | `tasks/active_context.md` | ✅ Done |
| Tasks Plan | `tasks/tasks_plan.md` | ✅ Done (this file) |
| Lessons Learned | `.windsurf/rules/methodology/lessons-learned.md` | ✅ Initialized |
| Error Documentation | `.windsurf/rules/methodology/error-documentation.md` | ✅ Initialized |

---

## 5. Potential Improvements (Backlog)

| # | Improvement | Priority | Effort |
|---|------------|----------|--------|
| 1 | ~~Set up Vitest for frontend unit testing~~ | ~~High~~ | ✅ Done |
| 2 | ~~Set up Playwright for E2E testing~~ | ~~High~~ | ✅ Done |
| 3 | Add component tests (`LeadForm`, `Navbar`) | Medium | Medium |
| 4 | ~~Add service tests (`EmailService`)~~ | ~~Medium~~ | ✅ Done |
| 5 | Add SEO meta tags per program page | Medium | Medium |
| 6 | Evaluate SSR/SSG (Next.js migration or prerendering) | Medium | High |
| 7 | Implement user authentication for admin features | Medium | Medium |
| 8 | ~~Wire django_attachments~~ | ~~Low~~ | Removed in cleanup |
| 9 | Add Zod or similar frontend validation | Low | Low |
| 10 | Set up i18n if English version needed | Low | High |
| 11 | Clean up empty `auth_utils.py` | Low | Trivial |
| 12 | Add structured data (JSON-LD) for programs | Medium | Low |

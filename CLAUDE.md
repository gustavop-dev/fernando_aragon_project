# Fernando Aragón — Claude Compatibility Guide

## Source Of Truth
- The canonical repo guidance is maintained in the Codex-native surfaces: `AGENTS.md`, `backend/AGENTS.md`, `frontend/AGENTS.md`, `.agents/skills/*`, `.codex/config.toml`.
- This `CLAUDE.md` file is a compatibility mirror for mixed-tool teams and should stay aligned with the Codex guidance.
- Long-lived project context lives in `docs/methodology/` and `tasks/`.

## Project Overview
- **What it is**: an educational/institutional landing site for Fernando Aragón school (`fernandodearagon.edu.co`). The visible product is the React SPA; the backend exists almost exclusively to serve a contact form and a reCAPTCHA verification endpoint.
- **Stack**: Django 6.0.2 + DRF (backend) / **React 18.3 + Vite 7 + TypeScript 5.5** (frontend) / MySQL / Redis / Huey / SMTP email.
- **Single Django app**: `base_feature_app`. Django module name is **`base_feature_project`** (a generic boilerplate name). Settings module: `base_feature_project.settings_prod`.
- **Production path**: `/home/ryzepeck/webapps/fernando_aragon_project`.
- **Domain**: `fernandodearagon.edu.co`.
- **Services**: `fernando_aragon_project.service`, `fernando-aragon-huey.service`. Socket: `/home/ryzepeck/webapps/fernando_aragon_project/fernando_aragon_project.sock`.
- The frontend Vite build emits to `backend/static/frontend/` and is served by Django.

## Architecture Invariants
- **Backend views are 100% function-based** with `@api_view`. There are only 3 endpoints: `submit_contact_form`, `verify_captcha`, `get_site_key`. Do not introduce CBV/`APIView`/`ViewSets`.
- **Service layer**: email logic lives in `base_feature_app/services/email_service.py`. Do not inline `send_mail()` calls into views.
- **Custom email-based User**: `User(AbstractBaseUser, PermissionsMixin)` with email as the username field. Roles `CUSTOMER`/`ADMIN` exist but only `ADMIN` is actively used.
- **Frontend uses React 18 + Vite + TypeScript**. **NOT React 19**, **NOT Next.js**.
- **No state management library**: state is `useState` only. There is no Zustand, Redux, or global Context.
- **HTTP**: native `fetch` (no Axios). Single API helper at `frontend/src/app/services/api.ts`. Base URL via `import.meta.env.VITE_API_URL`.
- **Bilingual via duplicated routes**: there is **no i18n framework**. Spanish content lives at `/`, English at `/ingles`. Both are React components with content forked.
- **shadcn/ui + Material UI + Radix**: a mixed UI library setup. shadcn components live in `frontend/src/app/components/ui/`. Material UI is also pulled in via `@mui/material`.
- **Conditional Silk** profiling: gated by `ENABLE_SILK=True`. Off by default.

## Working Rules
- Prefer existing project patterns over generic framework advice.
- Do not rename `base_feature_project` or `base_feature_app` to `fernando_aragon_*` — they are intentionally generic.
- Do not introduce a state management library or i18n framework unless the user explicitly asks. The current scope is small and `useState` + duplicated routes is sufficient.
- Do not change old migrations; add new migrations when schema changes are required.
- Keep security basics intact: validated serializer inputs, ORM-first queries, escaped rendering, secure cookies, no secrets in code.
- Do not edit files inside `backend/static/frontend/` — they are Vite build artifacts.
- New email types should be added as methods on `EmailService`, not inlined.

## Commands
- Backend tests: `cd backend && source venv/bin/activate && pytest base_feature_app/tests/path/to/test_file.py -v`
- Backend dev server: `cd backend && source venv/bin/activate && python manage.py runserver`
- Frontend dev server: `cd frontend && npm run dev` (Vite, default :5173)
- Frontend unit tests (Vitest): `cd frontend && npm test -- path/to/file.test.tsx`
- Frontend E2E (Playwright): `cd frontend && npm run e2e -- path/to/spec.ts`
- Frontend build: `cd frontend && npm run build`

## Testing Constraints
- Never run the full test suite.
- Maximum 20 tests per batch and 3 test commands per cycle.
- Run only the smallest backend, frontend unit, or E2E slice needed for the changed behavior.

## Memory Bank
- Core files: `docs/methodology/{product_requirement_docs,architecture,technical,error-documentation,lessons-learned}.md`, `tasks/{tasks_plan,active_context}.md`.
- Update memory files when the user asks, or when you have verified a meaningful change to runtime surfaces, architecture, or recurring workflow guidance.
- Do not churn memory files after every routine code edit.

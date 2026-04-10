# Fernando Aragon — Codex AGENTS Configuration

## Project Identity

### Codex Runtime Surfaces
- **Primary instructions**: `AGENTS.md` (root scope) + `backend/AGENTS.md` + `frontend/AGENTS.md`
- **Skills (canonical)**: `.agents/skills/<skill>/SKILL.md` + `agents/openai.yaml`
- **Project config**: `.codex/config.toml`

- **Name**: Fernando Aragon
- **Domain**: `fernandodearagon.edu.co` / `www.fernandodearagon.edu.co`
- **Stack**: Django 6.0.2 + DRF (backend) / React 18.3 + Vite 7 SPA (frontend) / MySQL 8 / Redis / Huey
- **Server path**: `/home/ryzepeck/webapps/fernando_aragon_project`
- **Services**: `fernando_aragon_project.service` (Gunicorn), `fernando_aragon_project.socket`, `fernando-aragon-huey.service`
- **Settings module**: `DJANGO_SETTINGS_MODULE=base_feature_project.settings_prod`
- **Nginx**: `/etc/nginx/sites-available/fernando_aragon_project`
- **Static**: `/home/ryzepeck/webapps/fernando_aragon_project/backend/staticfiles/`
- **Media**: `/home/ryzepeck/webapps/fernando_aragon_project/backend/media/`
- **Resource limits**: MemoryMax=250M, CPUQuota=40%, OOMScoreAdjust=300

---

## General Rules

These should be respected ALWAYS:
1. Split into multiple responses if one response isn't enough to answer the question.
2. IMPROVEMENTS and FURTHER PROGRESSIONS:
- S1: Suggest ways to improve code stability or scalability.
- S2: Offer strategies to enhance performance or security.
- S3: Recommend methods for improving readability or maintainability.
- Recommend areas for further investigation

---

## Security Rules — OWASP / Secrets / Input Validation

### Secrets and Environment Variables

NEVER hardcode secrets. Always use environment variables.

```python
# ✅ Django — use env vars
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
DATABASE_URL = os.environ['DATABASE_URL']
STRIPE_API_KEY = os.environ['STRIPE_SECRET_KEY']

# ❌ NEVER do this
SECRET_KEY = 'django-insecure-abc123xyz'
DATABASE_URL = 'mysql://root:password123@localhost/mydb'
```

```typescript
// ✅ Next.js / Nuxt — use env vars
const apiUrl = process.env.NEXT_PUBLIC_API_URL
const secretKey = process.env.API_SECRET_KEY  // server-only, no NEXT_PUBLIC_ prefix

// Nuxt
const config = useRuntimeConfig()
const apiKey = config.apiSecret  // server only
const publicUrl = config.public.apiBase  // client safe

// ❌ NEVER do this
const API_KEY = 'sk-live-abc123xyz'
fetch('https://api.stripe.com/v1/charges', {
  headers: { Authorization: 'Bearer sk-live-abc123xyz' }
})
```

### .env rules

- `.env` files MUST be in `.gitignore`. Always verify before committing
- Use `.env.example` with placeholder values for documentation
- Separate env files per environment: `.env.local`, `.env.staging`, `.env.production`
- Server secrets (API keys, DB passwords) NEVER go in client-side env vars
- In Next.js: only `NEXT_PUBLIC_*` vars are exposed to the browser
- In Nuxt: only `runtimeConfig.public.*` is exposed to the browser

### Input Validation

NEVER trust user input. Validate on both server AND client.

#### Django/DRF

```python
# ✅ Serializer validates input
class OrderSerializer(serializers.Serializer):
    email = serializers.EmailField()
    quantity = serializers.IntegerField(min_value=1, max_value=100)
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError('Product not found')
        return value

# ❌ Using raw request data
def create_order(request):
    product_id = request.data['product_id']  # no validation
    Order.objects.create(product_id=product_id)  # SQL injection risk
```

#### React/Vue

```typescript
// ✅ Validate before sending
import { z } from 'zod'

const orderSchema = z.object({
  email: z.string().email(),
  quantity: z.number().int().min(1).max(100),
  productId: z.number().int().positive(),
})

const handleSubmit = (data: unknown) => {
  const result = orderSchema.safeParse(data)
  if (!result.success) {
    setErrors(result.error.flatten().fieldErrors)
    return
  }
  await submitOrder(result.data)
}
```

### SQL Injection Prevention

```python
# ✅ Django ORM — always safe
users = User.objects.filter(email=user_input)

# ✅ If raw SQL is needed, use parameterized queries
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM users WHERE email = %s", [user_input])

# ❌ NEVER interpolate user input into SQL
cursor.execute(f"SELECT * FROM users WHERE email = '{user_input}'")
```

### XSS Prevention

```typescript
// ✅ React auto-escapes by default — JSX is safe
return <p>{userInput}</p>

// ✅ Vue auto-escapes with {{ }}
// <p>{{ userInput }}</p>

// ❌ NEVER use dangerouslySetInnerHTML with user input
return <div dangerouslySetInnerHTML={{ __html: userInput }} />

// ❌ NEVER use v-html with user input
// <div v-html="userInput" />

// If you MUST render HTML, sanitize first
import DOMPurify from 'dompurify'
const clean = DOMPurify.sanitize(userInput)
```

### CSRF Protection

```python
# ✅ Django — CSRF middleware is on by default, keep it
MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',  # NEVER remove
    ...
]

# ✅ DRF — use SessionAuthentication or JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

# ❌ NEVER disable CSRF globally
@csrf_exempt  # only for webhooks from external services with signature verification
```

### Authentication and Authorization

```python
# ✅ Always check permissions
from rest_framework.permissions import IsAuthenticated

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users can only see their own orders
        return Order.objects.filter(user=self.request.user)
```

### Sensitive Data Exposure

```python
# ✅ Exclude sensitive fields from serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']
        # password, tokens, internal IDs are excluded

# ❌ Exposing everything
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  # leaks password hash, tokens, etc.
```

### HTTP Security Headers (Django)

```python
# settings.py — enable all security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True  # in production
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
```

### Dependency Security

- Run `pip audit` (Python) and `npm audit` (Node) regularly
- Never use `*` for dependency versions — pin exact versions
- Review new dependencies before adding them
- Keep dependencies updated, especially security patches

### File Upload Security

```python
# ✅ Validate file type and size
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.pdf'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def validate_upload(file):
    ext = Path(file.name).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(f'File type {ext} not allowed')
    if file.size > MAX_FILE_SIZE:
        raise ValidationError('File too large')
```

### Security Checklist — Before Every Deployment

- [ ] No secrets in code or git history
- [ ] `.env` is in `.gitignore`
- [ ] All user input is validated (server + client)
- [ ] No raw SQL with user input
- [ ] No `dangerouslySetInnerHTML` / `v-html` with user data
- [ ] CSRF protection enabled
- [ ] Authentication required on all sensitive endpoints
- [ ] Serializers exclude sensitive fields
- [ ] Security headers configured
- [ ] `pip audit` / `npm audit` clean
- [ ] File uploads validated
- [ ] DEBUG = False in production
- [ ] ALLOWED_HOSTS configured properly

---

## Memory Bank System

Fernando Aragón maintains a Memory Bank under `docs/methodology/` and `tasks/`. Read these files before significant implementation, debugging, or planning work.

```mermaid
flowchart TD
    PB[product_requirement_docs.md] --> PC[technical.md]
    PB --> SP[architecture.md]
    SP --> TC[tasks_plan.md]
    PC --> TC
    PB --> TC
    TC --> AC[active_context.md]
    AC --> ER[error-documentation.md]
    AC --> LL[lessons-learned.md]
```

### Core Files

| # | File | Purpose |
|---|------|---------|
| 1 | `docs/methodology/product_requirement_docs.md` | Functional requirements for the educational landing site |
| 2 | `docs/methodology/architecture.md` | System diagram (Django backend, React SPA, Huey async) |
| 3 | `docs/methodology/technical.md` | Tech decisions and patterns |
| 4 | `docs/methodology/error-documentation.md` | Known errors and resolutions |
| 5 | `docs/methodology/lessons-learned.md` | Implementation learnings |
| 6 | `tasks/tasks_plan.md` | Feature roadmap |
| 7 | `tasks/active_context.md` | Current execution context |

### When to Read

- Before significant implementation: read `architecture.md`, `technical.md`, and the relevant `lessons-learned.md` section.
- Before planning: read `tasks_plan.md` and `active_context.md`.
- When debugging: check `error-documentation.md` first.

### When to Update

1. After verifying a new project pattern (add to `lessons-learned.md`).
2. After implementing significant changes (update `tasks_plan.md`).
3. When the user requests with **update memory files** (review all core files).
4. After a significant part of a plan is verified (update `active_context.md`).

Do not churn memory files after every routine code edit.

---

## Directory Structure

```mermaid
flowchart TD
    Root[Project Root]
    Root --> Backend[backend/ — Django + DRF]
    Root --> Frontend[frontend/ — React + Vite SPA + TypeScript]
    Root --> Docs[docs/]
    Root --> Tasks[tasks/]
    Root --> Scripts[scripts/]
    Root --> AgentSkills[.agents/skills/]

    Backend --> BBaseFeatureApp[base_feature_app/ — single business app: User, contact form, captcha]
    Backend --> BBaseFeatureProj[base_feature_project/ — Django project module]
    Backend --> BConftest[conftest.py + pytest.ini]
    Backend --> BMedia[media/ + staticfiles/]

    BBaseFeatureApp --> Models[models.py — custom email-based User]
    BBaseFeatureApp --> Views[views/ — FBV @api_view: contact form, recaptcha verify, sitekey]
    BBaseFeatureApp --> Services[services/ — EmailService]
    BBaseFeatureApp --> Tests[tests/ — pytest + coverage]

    Frontend --> FApp[src/app/ — App.tsx, routes.ts]
    FApp --> FComponents[components/ — Layout, Navbar, Footer, LeadForm, CelacCertificates, AnimatedCounter, etc.]
    FApp --> FUI[components/ui/ — shadcn library 45+ components]
    FApp --> FPages[pages/ — Home.tsx, English.tsx, ProgramPage.tsx]
    FApp --> FServices[services/ — api.ts (fetch native, no axios)]
    FApp --> FData[data/ — programs.ts, curriculum.ts]
    FApp --> FAssets[assets/ — SVG, images]
    Frontend --> FTests[src/__tests__/ — Vitest + Playwright]

    AgentSkills --> SkillSet[plan, implement, debug, deploy-and-check, deploy-staging, git-commit, etc.]
```

**Important note on naming**: the **Django project module is `base_feature_project`** (a base/boilerplate module name), and the **Django app is `base_feature_app`**. The directory `fernando_aragon_project/` houses these. Settings module is `base_feature_project.settings_prod`. Do not rename these to `fernando_aragon_*` — keep the boilerplate names.

---

## Testing Rules

### Execution Constraints

- **Never run the full test suite** — always specify files.
- **Maximum per execution**: 20 tests per batch, 3 commands per cycle.
- **Backend**: `cd backend && source venv/bin/activate && pytest base_feature_app/tests/path/to/test_file.py -v`. `pytest.ini` already sets `DJANGO_SETTINGS_MODULE` and adds `--cov=base_feature_app`.
- **Frontend unit (Vitest)**: `cd frontend && npm test -- path/to/file.test.tsx`. Tests live under `frontend/src/__tests__/`.
- **Frontend E2E (Playwright)**: `cd frontend && npx playwright test e2e/path/to/spec.ts` — max 2 files per invocation. Use `E2E_REUSE_SERVER=1` when a Vite dev server is already running.

### Quality Standards

Full reference: `docs/TESTING_QUALITY_STANDARDS.md`

- Each test verifies **ONE specific behavior**
- **No conjunctions** in test names — split into separate tests
- Assert **observable outcomes** (status codes, DB state, rendered UI)
- **No conditionals** in test body — use parameterization
- Follow **AAA pattern**: Arrange → Act → Assert
- Mock only at **system boundaries** (external APIs, clock, email)

---

## Lessons Learned — Fernando Aragón

### Architecture Patterns

#### Minimal landing site, single business app
- Fernando Aragón is an **educational/institutional landing site** for a school (`fernandodearagon.edu.co`).
- The backend has a single business app: `base_feature_app`. There is **no e-commerce, no auth flows, no CRUD** beyond a contact form and reCAPTCHA verification.
- The Django project module is named **`base_feature_project`** — a generic boilerplate name. Do not rename it.

#### Boilerplate base
- Both the project module (`base_feature_project`) and the app (`base_feature_app`) are named after a "base feature" template. This suggests the user maintains a reusable boilerplate that gets customized per landing project (Tuhuella also uses `base_feature_project` as its module name).
- Treat this repo as a thin specialization of that template — most of the value lives in the React frontend.

#### Service layer for email
- `base_feature_app/services/email_service.py` centralizes email logic.
- `EmailService.send_contact_notification()` is the canonical entry point: it composes the contact-form notification and sends it to the admin via SMTP.
- New email types should be added as methods on `EmailService`, not inlined into views.

#### Huey periodic tasks
- All scheduled work lives in `backend/base_feature_project/tasks.py`:
  - `scheduled_backup` — Sun 03:30 UTC (DB + media, weekly retention 4).
  - `silk_garbage_collection` — daily 04:15 UTC (no-op when Silk is off).
  - `weekly_slow_queries_report` — Fri 07:30 UTC.
  - `silk_reports_cleanup` — 1st of month 05:15 UTC.
- In dev (`HUEY['immediate']=True`), tasks run synchronously and no Huey worker is required.

#### Conditional Silk
- `django-silk` is gated by `ENABLE_SILK=True`. Off by default.

### Code Style & Conventions

#### Backend: 100% function-based views
- The 3 existing views (`submit_contact_form`, `verify_captcha`, `get_site_key`) are **function-based with `@api_view`**.
- Pattern: deserialize → validate → call service → respond.
- Permissions: `AllowAny` (public landing endpoints).
- Never convert to CBV/`APIView`/`ViewSets` unless explicitly requested.

#### Backend: custom email-based User
- `User` extends `AbstractBaseUser + PermissionsMixin` with email as the username field.
- Roles: `CUSTOMER` and `ADMIN` (only the admin role is actively used; the landing has no end-user accounts).
- Custom `UserManager` with `create_user`/`create_superuser`.

#### Frontend: React 18 + Vite + TypeScript
- **React 18.3.1**, not 19. **Vite 7**. **TypeScript 5.5**.
- Routing: **`react-router` 7** with `createBrowserRouter` and a `Layout` boundary. Routes: `/` (Home), `/ingles` (English version), `/:slug` (per-program detail page).
- **No state management library** — all state is local `useState`. There is no Zustand, no Redux, no global Context.
- **HTTP**: native `fetch` (no Axios). The single API helper is `src/app/services/api.ts` with `submitContactForm()` and `ContactFormData` interface. Base URL via `import.meta.env.VITE_API_URL`.
- **Forms**: `react-hook-form` 7.55 is installed but the actual contact form uses local `useState` (the component is `LeadForm.tsx`).
- **i18n**: there is **no i18n framework**. Bilingual content is handled by **separate routes** (`/` for Spanish, `/ingles` for English) with content duplicated per page.

#### Frontend: UI library mix
- **shadcn/ui** components live in `src/app/components/ui/` (~45 components: accordion, dialog, button, form, input, etc.) — these are pre-installed and customizable.
- **Material UI 7.3** + **@emotion/react / @emotion/styled** for some components.
- **Radix UI** primitives (25+ packages) underlying shadcn.
- **Tailwind CSS 4.1** + **`@tailwindcss/vite`** plugin.
- **Animations**: `motion` (Framer Motion) 12.23 with `useInView` for lazy scroll-triggered animations on `motion.div` / `motion.section`.
- **Icons**: `lucide-react`.
- **Charts**: `recharts`.
- **Carousels**: `swiper` + `embla-carousel-react`.
- **Date pickers**: `react-day-picker` + `date-fns` 3.6.
- **Toasts**: `sonner`.
- **Dark mode**: `next-themes`.

#### Frontend naming
- Components: PascalCase (`Layout.tsx`, `LeadForm.tsx`, `AnimatedCounter.tsx`).
- shadcn UI files: kebab-case (`accordion.tsx`, `dialog.tsx`).
- Functions and state: camelCase.

### Development Workflow

#### venv lives in `backend/`
```bash
cd backend && source venv/bin/activate
```

#### Frontend dev server
```bash
cd frontend && npm install && npm run dev   # Vite, default :5173
```

### Production Deployment

See `.agents/skills/deploy-and-check/SKILL.md`. Summary:
1. `git pull origin master`
2. Backend: `cd backend && source venv/bin/activate && pip install -r requirements.txt && python manage.py migrate`
3. Frontend: `cd frontend && npm ci && npm run build`
4. Backend: `python manage.py collectstatic --noinput`
5. Restart: `sudo systemctl restart fernando_aragon_project && sudo systemctl restart fernando-aragon-huey`
6. Verify: `bash /home/ryzepeck/webapps/ops/vps/scripts/deployment/post-deploy-check.sh fernando_aragon_project`

The systemd unit name is `fernando_aragon_project.service` (with the underscore-named directory). The socket lives at `/home/ryzepeck/webapps/fernando_aragon_project/fernando_aragon_project.sock`.

### Testing Insights

- **Backend**: pytest 9 + pytest-django + pytest-cov. Tests under `backend/base_feature_app/tests/` covering views (contact, captcha), commands (huey tasks), and utils (admin, settings, forms, urls).
- **Frontend unit**: **Vitest** 4.1 + React Testing Library 16.3 + jsdom. Tests under `frontend/src/__tests__/`.
- **Frontend E2E**: Playwright 1.58 with `npm run e2e`, `e2e:headed`, `e2e:clean`.
- **Quality gate**: `scripts/test_quality_gate.py`.

### Tech Debt / Things to Be Aware Of

- Bilingual content lives in **duplicated routes** (`/` vs `/ingles`) rather than in i18n locale files. Adding a third language would require a new route and content fork.
- `react-hook-form` is installed but unused — the contact form uses local `useState`.
- The `User` model has roles (`CUSTOMER`, `ADMIN`) but only `ADMIN` is actively used.

---

## Error Documentation — Fernando Aragón

### Known Issues

_No known issues recorded yet. When a bug is discovered that warrants long-lived documentation, add it here with the format:_

```
#### [KNOWN-NNN] short title
- **Context**: ...
- **Workaround**: ...
```

### Resolved Issues

_No resolved issues recorded yet. When fixing a non-trivial bug, document the root cause and resolution here:_

```
#### [ERR-NNN] short title
- ...
- **Resolution**: ...
```

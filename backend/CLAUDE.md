# Backend Rules — Fernando Aragón

## Stack And Scope
- Django 6.0.2 + DRF 3.16.1, Python 3.12.
- **Single business app**: `base_feature_app` — contains the custom `User` model (email-based, roles `CUSTOMER`/`ADMIN`), the contact-form views, the reCAPTCHA verification view, and the email service.
- **Django project module**: `base_feature_project` (a generic boilerplate name; do not rename).
- **Production settings module**: `base_feature_project.settings_prod`.
- Database: per `projects.yml`, MySQL (`fernando_aragon_db`). Cache + queue: Redis. Email: SMTP.

## Project Conventions
- DRF views are **function-based** with `@api_view`. The 3 existing endpoints are `submit_contact_form`, `verify_captcha`, and `get_site_key`. Pattern: deserialize → service call → respond. Permissions: `AllowAny`.
- **Service layer**: `base_feature_app/services/email_service.py` centralizes email logic (`EmailService.send_contact_notification`). Add new email types as methods on `EmailService`.
- **Custom User model**: `User(AbstractBaseUser, PermissionsMixin)` with email as the username field, custom `UserManager`. Roles: `CUSTOMER`, `ADMIN` (only `ADMIN` is actively used).
- There are **no models beyond `User`** yet. The contact form is processed via DRF serializers without persistence.
- Prefer Django ORM. Raw SQL only when strictly necessary, always parameterized.

## Auth And Security
- Admin uses Django session + CSRF.
- Public landing endpoints (`/api/contact/submit/`, `/api/google-captcha/verify/`, `/api/google-captcha/sitekey/`) are unauthenticated (`AllowAny`).
- `settings_prod.py` enforces HSTS (1y, subdomains, preload), `SECURE_SSL_REDIRECT=True`, secure cookies, NOSNIFF, `X_FRAME_OPTIONS=DENY`, fail-fast on missing `DJANGO_SECRET_KEY` / `DJANGO_ALLOWED_HOSTS`.
- The `EMAIL_BACKEND` is `django.core.mail.backends.smtp.EmailBackend` (required in prod).
- reCAPTCHA is verified server-side via `verify_captcha` before processing the contact form.
- Validate input in DRF serializers. Never disable CSRF or hardcode secrets.

## Commands
- Activate venv from `backend/`: `cd backend && source venv/bin/activate`
- Run backend tests: `pytest base_feature_app/tests/path/to/test_file.py -v`
- Run a focused backend check: `python manage.py check`
- Run dev server: `python manage.py runserver`
- Make migrations: `python manage.py makemigrations base_feature_app && python manage.py migrate`

## Testing Rules
- Run only the changed test file or a tight regression slice.
- Never run the full backend suite.
- Keep test names focused on one observable behavior.
- Prefer deterministic tests: freeze time, seed data explicitly, and avoid hidden global state.
- Test directories: `base_feature_app/tests/views/`, `base_feature_app/tests/commands/`, `base_feature_app/tests/utils/`.

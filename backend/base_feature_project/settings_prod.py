"""
Production settings for base_feature_project.

Usage: DJANGO_SETTINGS_MODULE=base_feature_project.settings_prod

This file is imported AFTER settings.py (base). All shared configuration
lives in settings.py; this file only contains production overrides and
validations.
"""

from decouple import config

from .settings import *  # noqa: F401,F403

# ---------------------------------------------------------------------------
# Core safety: DEBUG is always False in production
# ---------------------------------------------------------------------------
DEBUG = False

# ---------------------------------------------------------------------------
# Required environment variables — fail fast if missing
# ---------------------------------------------------------------------------
if not config('DJANGO_SECRET_KEY', default=''):
    raise ValueError("DJANGO_SECRET_KEY is required in production")

if not config('DJANGO_ALLOWED_HOSTS', default=''):
    raise ValueError("DJANGO_ALLOWED_HOSTS is required in production")

# ---------------------------------------------------------------------------
# Security hardening
# ---------------------------------------------------------------------------
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# ---------------------------------------------------------------------------
# Production email — require SMTP backend
# ---------------------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# ---------------------------------------------------------------------------
# Production logging — add file handler
# ---------------------------------------------------------------------------
LOGGING['handlers']['file'] = {  # noqa: F405
    'level': 'WARNING',
    'class': 'logging.handlers.RotatingFileHandler',
    'filename': BASE_DIR / 'logs' / 'django.log',  # noqa: F405
    'maxBytes': 5 * 1024 * 1024,
    'backupCount': 3,
    'formatter': 'verbose',
}
LOGGING['loggers']['django']['handlers'].append('file')  # noqa: F405

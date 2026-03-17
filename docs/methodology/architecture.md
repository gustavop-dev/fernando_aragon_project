# Architecture — Corporación Fernando de Aragón

## 1. System Overview

```mermaid
flowchart TB
    subgraph Client["Browser (SPA)"]
        React["React 18 + Vite 6"]
        RR["React Router 7"]
        TW["TailwindCSS 4"]
        Shadcn["shadcn/ui (46 components)"]
    end

    subgraph Server["Django Backend"]
        DRF["Django REST Framework 3.16"]
        Views["Function-based Views"]
        Services["Service Layer"]
        Models["Django ORM"]
        Admin["Custom Admin Site"]
    end

    subgraph Infra["Infrastructure"]
        DB[(SQLite / MySQL)]
        Redis["Redis"]
        Huey["Huey Task Queue"]
        SMTP["SMTP (Gmail)"]
        Captcha["Google reCAPTCHA"]
    end

    React -->|HTTP/JSON| DRF
    DRF --> Views
    Views --> Services
    Services --> Models
    Services --> SMTP
    Views --> Captcha
    Models --> DB
    Huey --> Redis
    Huey -->|Scheduled tasks| DB
    Huey --> SMTP
    Admin --> Models
```

---

## 2. Development Architecture

```mermaid
flowchart LR
    subgraph Dev["Development Environment"]
        ViteDev["Vite Dev Server\n:5173"]
        DjangoDev["Django runserver\n:8000"]
    end

    subgraph Tools["Quality Tooling"]
        Pytest["pytest + coverage"]
        Ruff["Ruff linter"]
        PreCommit["pre-commit hooks"]
        QualityGate["test_quality_gate.py"]
        GHA["GitHub Actions CI"]
    end

    ViteDev -->|CORS| DjangoDev
    PreCommit --> QualityGate
    GHA --> QualityGate
    QualityGate --> Pytest
    QualityGate --> Ruff
```

---

## 3. Request Flow

```mermaid
sequenceDiagram
    participant B as Browser (React)
    participant V as Vite Dev Server
    participant D as Django API
    participant S as EmailService
    participant G as Google reCAPTCHA
    participant M as SMTP Server

    Note over B: User fills lead form
    B->>V: SPA page load (/:slug)
    V-->>B: React app + program data

    B->>D: POST /api/contact/submit/
    D->>D: ContactFormSerializer.validate()

    alt captcha_token provided
        D->>G: POST siteverify (token)
        G-->>D: {success: true/false}
    end

    D->>S: EmailService.send_contact_notification()
    S->>M: send_mail()
    M-->>S: OK
    S-->>D: True
    D-->>B: {success: true, detail: "Mensaje enviado"}
```

---

## 4. Entity-Relationship Diagram

```mermaid
erDiagram
    USER {
        bigint id PK
        varchar email UK "USERNAME_FIELD"
        varchar first_name
        varchar last_name
        varchar phone
        varchar role "customer | admin"
        boolean is_active
        boolean is_staff
        boolean is_superuser
        datetime date_joined
        datetime last_login
        varchar password
    }

```

**Notes:**
- `User` is the only model in the project (`base_feature_app`) — custom model with email as identifier
- `django_attachments` was removed during cleanup (2026-03-17) — it was unused code

---

## 5. Model Details

### base_feature_app.User

| Field | Type | Constraints |
|-------|------|-------------|
| `id` | BigAutoField | PK |
| `email` | EmailField | unique, USERNAME_FIELD |
| `first_name` | CharField(150) | blank |
| `last_name` | CharField(150) | blank |
| `phone` | CharField(50) | blank |
| `role` | CharField(20) | choices: `customer` (default), `admin` |
| `is_active` | BooleanField | default=True |
| `is_staff` | BooleanField | default=False |
| `is_superuser` | BooleanField | inherited from PermissionsMixin |
| `date_joined` | DateTimeField | default=timezone.now |
| `password` | CharField | inherited from AbstractBaseUser |
| `last_login` | DateTimeField | inherited from AbstractBaseUser |

**Manager**: `UserManager` — custom `create_user()` and `create_superuser()` methods

---

## 6. Service Layer

```mermaid
flowchart TD
    subgraph Views["Views (Function-based)"]
        CV["contact.submit_contact_form"]
        CAP["captcha_views.get_site_key\ncaptcha_views.verify_captcha"]
    end

    subgraph Serializers
        CFS["ContactFormSerializer"]
    end

    subgraph Services
        ES["EmailService.send_contact_notification()"]
    end

    subgraph External
        SMTP["Django send_mail → SMTP"]
        GCAP["Google reCAPTCHA API"]
    end

    CV --> CFS
    CV --> ES
    CV --> CAP
    CAP --> GCAP
    ES --> SMTP
```

---

## 7. Page Routing & Frontend Architecture

```mermaid
flowchart TD
    subgraph Router["React Router 7"]
        Root["/ (Layout)"]
        Root --> Home["/ → Home.tsx"]
        Root --> English["/ingles → English.tsx"]
        Root --> Program["/:slug → ProgramPage.tsx"]
    end

    subgraph Layout["Layout.tsx"]
        Navbar["Navbar"]
        Outlet["<Outlet />"]
        Footer["Footer"]
        WA["WhatsAppButton"]
    end

    subgraph Shared["Shared Components"]
        LF["LeadForm"]
        AC["AnimatedCounter"]
        CS["CurriculumSection"]
    end

    subgraph Data["Static Data"]
        PD["programs.ts (15 programs)"]
        CD["curriculum.ts (modules per program)"]
    end

    subgraph API["API Client"]
        ApiTs["services/api.ts"]
    end

    Home --> LF
    English --> LF
    Program --> LF
    Program --> CS
    Home --> AC
    LF --> ApiTs
    Program --> PD
    Program --> CD
    ApiTs -->|POST /api/contact/submit/| Backend["Django API"]
```

---

## 8. Scheduled Tasks Architecture

```mermaid
flowchart LR
    subgraph Huey["Huey Task Queue"]
        Backup["scheduled_backup\n(weekly, Sun 3:30 AM)"]
        Silk["silk_garbage_collection\n(daily, 4:15 AM)"]
        Report["weekly_slow_queries_report\n(Fri 7:30 AM)"]
    end

    subgraph Actions
        DBBackup["django-dbbackup\n(DB + media)"]
        SilkGC["silk_garbage_collect\n(7-day retention)"]
        SilkReport["Query performance\nreport to logs/"]
    end

    Redis["Redis :6379/1"] --> Huey
    Backup --> DBBackup
    Silk --> SilkGC
    Report --> SilkReport
```

---

## 9. Deployment Architecture (Production)

```mermaid
flowchart TB
    subgraph Production["Production Server"]
        Django["Django\n(settings_prod.py)"]
        Huey_Worker["Huey Worker\n(systemd service)"]
        Redis_Prod["Redis"]
        MySQL["MySQL Database"]
        Static["Static Files\n(/staticfiles/)"]
        Media["Media Files\n(/media/)"]
        Backups["Backup Storage\n(BACKUP_STORAGE_PATH)"]
    end

    subgraph External["External Services"]
        SMTP_Prod["SMTP (Gmail)"]
        reCAPTCHA["Google reCAPTCHA"]
    end

    subgraph Security["Security Headers"]
        HSTS["HSTS (1 year)"]
        SSL["SSL Redirect"]
        XFrame["X-Frame: DENY"]
        XSS["XSS Filter"]
        NoSniff["Content-Type Nosniff"]
    end

    Django --> MySQL
    Django --> Static
    Django --> Media
    Django --> SMTP_Prod
    Django --> reCAPTCHA
    Huey_Worker --> Redis_Prod
    Huey_Worker --> MySQL
    Huey_Worker --> Backups
    Django --> Security
```

**Production requirements** (enforced by `settings_prod.py`):
- `DJANGO_SECRET_KEY` must be set
- `DJANGO_ALLOWED_HOSTS` must be set
- `DEBUG = False` always
- SMTP email backend required
- All security headers enabled

---

## 10. API Endpoints Summary

| Method | Endpoint | Permission | Description |
|--------|----------|------------|-------------|
| `GET` | `/api/health/` | AllowAny | Health check |
| `POST` | `/api/contact/submit/` | AllowAny | Submit lead form |
| `GET` | `/api/google-captcha/site-key/` | AllowAny | Get reCAPTCHA site key |
| `POST` | `/api/google-captcha/verify/` | AllowAny | Verify captcha token |
| — | `/admin/` | Staff | Custom admin site |
| — | `/admin-gallery/` | Staff | Default Django admin |

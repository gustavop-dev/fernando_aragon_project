# Product Requirement Document — Corporación Fernando de Aragón

## 1. Overview

**Corporación Fernando de Aragón** is a Colombian educational institution offering 15 technical and vocational programs. This project is their **lead generation website** — a public-facing SPA designed to maximize SEO relevance and ad conversion through dedicated landing pages per program, each with integrated lead capture forms and WhatsApp CTAs.

The site follows a **one landing page per program** model to drive organic search traffic and paid ad conversions. Every page funnels visitors toward submitting a contact form or initiating a WhatsApp conversation.

---

## 2. Problems Solved

| Problem | Solution |
|---------|----------|
| No centralized digital presence for 15+ programs | Dedicated landing page per program with SEO-friendly slugs |
| Manual lead tracking via phone/WhatsApp only | Structured contact form submissions with email notifications |
| Spam and bot form submissions | Google reCAPTCHA integration on contact forms |
| No program comparison for prospective students | Unified program data (duration, modules, certification, curriculum) across pages |
| Difficulty reaching institution outside business hours | Floating WhatsApp CTA button available on every page |

---

## 3. Target Users

- **Primary**: Prospective students in Colombia looking for technical/vocational education
- **Secondary**: Parents and guardians researching programs for their children
- **Internal**: Administrative staff managing leads and program information

---

## 4. Core Features

### 4.1 Frontend (Public Website)

- **Home Page** — Hero section, institution stats (animated counters), featured programs carousel, testimonials, and lead capture form
- **English Program Page** — Dedicated landing page for the English program with CEFR level structure
- **Dynamic Program Pages** — Template-driven pages for all 15 programs, rendered by slug (e.g., `/auxiliar-primera-infancia`)
- **Lead Capture Form** — Contact form with fields: name, email, phone, program selector; supports light/dark variants and program pre-selection
- **WhatsApp CTA** — Floating button on every page linking to WhatsApp
- **Responsive Navbar** — Mobile-first navigation with programs dropdown
- **Curriculum Accordion** — Per-program curriculum module display with hours breakdown
- **Animated Counters** — Scroll-triggered statistics (students, years, programs, etc.)

### 4.2 Backend (API)

- **Contact Form Endpoint** — `POST /api/contact/submit/` receives lead data and sends email notification
- **reCAPTCHA Integration** — `GET /api/google-captcha/site-key/` and `POST /api/google-captcha/verify/`
- **Email Service** — Centralized service layer for sending contact notification emails to administrators
- **Health Check** — `GET /api/health/`
- **Custom User Model** — Email-based authentication with role system (customer/admin)
- **Django Admin** — Customized admin panel for user management

### 4.3 Infrastructure

- **Automated Backups** — Scheduled DB + media backups via Huey + Redis (weekly)
- **Query Profiling** — django-silk behind feature flag for performance monitoring
- **Silk Garbage Collection** — Daily cleanup of profiling data
- **Weekly Slow Query Report** — Automated performance report generation

---

## 5. Programs Offered (15 total)

| # | Program | Slug |
|---|---------|------|
| 1 | Programa de Inglés | `ingles` |
| 2 | Auxiliar en Educación para la Primera Infancia | `auxiliar-primera-infancia` |
| 3 | Auxiliar Judicial y de Tribunales | `auxiliar-tribunales` |
| 4 | Auxiliar en Operaciones Portuarias | `operaciones-portuarias` |
| 5 | Auxiliar Administrativo | `auxiliar-administrativo` |
| 6 | Auxiliar de Aduana | `auxiliar-aduana` |
| 7 | Auxiliar de Diseño y Producción Gráfica | `diseno-produccion-grafica` |
| 8 | Investigación Judicial y Criminalística | `investigacion-criminal` |
| 9 | Operador de Maquinaria de Equipo Pesado | `operador-equipo-pesado` |
| 10 | Patronaje, Corte y Confección | `patronaje-confeccion` |
| 11 | Servicio al Huésped con Énfasis en Hotelería | `servicio-huesped` |
| 12 | Técnico en Peluquería y Barbería | `peluqueria-barberia` |
| 13 | Auxiliar en Saneamiento Ambiental | `saneamiento-ambiental` |
| 14 | Auxiliar en Seguridad en el Trabajo | `seguridad-trabajo` |
| 15 | Asistencia y Soporte de Tecnologías de la Información | `soporte-ti` |

---

## 6. Non-Functional Requirements

- **Performance**: Fast page loads via Vite SPA with code splitting
- **SEO**: One page per program with meaningful slugs for organic search
- **Responsiveness**: Mobile-first design, all pages functional on mobile devices
- **Security**: reCAPTCHA spam protection, CORS configured, CSRF protection, production security headers (HSTS, XSS filter, content-type nosniff, X-Frame DENY)
- **Reliability**: Automated backups with configurable retention, health check endpoint
- **Monitoring**: Optional query profiling via django-silk, slow query detection
- **Maintainability**: Static program data in TypeScript files (no CMS needed), service layer pattern in backend

---

## 7. Business Rules

- **Lead Form**: All fields (name, email, phone, program) are required
- **Captcha**: reCAPTCHA verification is optional — bypassed when keys are not configured (development mode)
- **Email Notifications**: Contact form submissions trigger email to configured administrator address (`CONTACT_NOTIFICATION_EMAIL`)
- **User Roles**: Two roles — `customer` (default) and `admin`
- **Program Data**: All program information is stored as static TypeScript data files, not in the database
- **Curriculum Data**: Module-level curriculum (name, hours, type) maintained per program in `curriculum.ts`
- **Backup Schedule**: Weekly automated backups (DB + media) with 4-backup retention (~1 month)
- **Silk Profiling**: Disabled by default, enabled via `ENABLE_SILK=true` environment variable; only intercepts `/api/` paths

---

## 8. Out of Scope (Current Phase)

- Student enrollment / registration system
- Payment processing
- User authentication for public visitors (no login required)
- CMS for program content management
- Multi-language support (site is in Spanish)
- Student portal / dashboard

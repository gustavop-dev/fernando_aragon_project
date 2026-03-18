# User Flow Map

**Single source of truth for all user flows in the Corporación Fernando de Aragón website.**

Use this document to understand each flow's steps, branching conditions, and API contracts before writing or reviewing E2E tests.

**Version:** 2.0.0
**Last Updated:** 2026-03

---

## Table of Contents

1. [Module Index](#module-index)
2. [Public Module](#public-module)
3. [Lead Capture Module](#lead-capture-module)
4. [Cross-Reference](#cross-reference)

---

## Module Index

| Flow ID | Name | Module | Priority | Roles | Frontend Route |
|---------|------|--------|----------|-------|----------------|
| `public-home` | Home Page | public | P1 | visitor | `/` |
| `public-navigation` | Site Navigation | public | P1 | visitor | all pages |
| `public-program-browse` | Browse Program | public | P1 | visitor | `/:slug` |
| `public-english-page` | English Program Page | public | P2 | visitor | `/ingles` |
| `lead-submit-form` | Submit Lead Form | lead-capture | P1 | visitor | `/`, `/:slug` |
| `lead-whatsapp-cta` | WhatsApp CTA | lead-capture | P2 | visitor | all pages |

---

## Public Module

### public-home

| Field | Value |
|-------|-------|
| **Priority** | P1 |
| **Roles** | visitor |
| **Frontend route** | `/` |
| **API endpoints** | None (static data) |

**Preconditions:** None.

**Steps:**

1. User navigates to `/`.
2. Page renders hero section with institution branding and CTA button.
3. Animated statistics section displays counters: 15+ Programs, 2500+ Graduates, 98% Employability, 20+ Years.
4. Featured programs section shows program cards with icons and descriptions.
5. Each program card links to its detail page (`/:slug`).
6. Testimonials section displays graduate reviews in a carousel.
7. Lead capture form (`LeadForm`) appears at the bottom of the page.
8. Page scrolls to top on navigation.

**Branching conditions:**

| Condition | Behavior |
|-----------|----------|
| Mobile viewport | Responsive layout; hamburger menu in navbar |
| Programs dropdown hover | Programs mega-menu opens in navbar |

---

### public-navigation

| Field | Value |
|-------|-------|
| **Priority** | P1 |
| **Roles** | visitor |
| **Frontend route** | all pages |
| **API endpoints** | None |

**Preconditions:** None.

**Steps:**

1. Every page renders a shared `Layout` with `Navbar`, `Footer`, and `WhatsAppButton`.
2. Navbar contains: logo (links to `/`), **Inicio** link, **Programas** dropdown (all 15+ programs), **Inglés** link, **Contacto** anchor.
3. Navbar becomes sticky and adds shadow on scroll (`scrollY > 20`).
4. On mobile: hamburger menu toggles a slide-out navigation panel.
5. Programs dropdown lists all programs from `programs.ts` data, each linking to `/:slug`.
6. Footer displays contact information, location, and institutional links.
7. `WhatsAppButton` floats on every page as a persistent CTA.
8. Page scrolls to top automatically on route change.

**Branching conditions:**

| Condition | Behavior |
|-----------|----------|
| Mobile viewport (`< 768px`) | Hamburger menu replaces horizontal nav; programs shown in collapsible accordion |
| Desktop viewport | Full horizontal nav with hover dropdown for programs |
| Click outside dropdown | Dropdown closes |

---

### public-program-browse

| Field | Value |
|-------|-------|
| **Priority** | P1 |
| **Roles** | visitor |
| **Frontend route** | `/:slug` |
| **API endpoints** | None (static data from `programs.ts`) |

**Preconditions:** Program slug exists in `programs` array.

**Steps:**

1. User clicks a program card on Home or selects a program from the Navbar dropdown.
2. React Router matches `/:slug` and renders `ProgramPage`.
3. Component looks up program data from `programs.ts` by slug.
4. Page renders:
   - Hero section with program name, description, and hero image.
   - Quick facts: duration, modules, modality, schedule, certification.
   - Program objective and graduate profile.
   - Functions and job titles list.
   - "Why study this program?" highlights.
   - `CurriculumSection` accordion with program modules (from `curriculum.ts`).
   - `LeadForm` pre-selected with this program's name.
5. User can submit the lead form (see `lead-submit-form` flow).

**Branching conditions:**

| Condition | Behavior |
|-----------|----------|
| Slug not found in `programs` | Page may render empty or show fallback |
| Program has no `jobTitles` | Job titles section hidden |
| Program has no curriculum data | Curriculum section hidden |

---

### public-english-page

| Field | Value |
|-------|-------|
| **Priority** | P2 |
| **Roles** | visitor |
| **Frontend route** | `/ingles` |
| **API endpoints** | None (static data) |

**Preconditions:** None.

**Steps:**

1. User navigates to `/ingles` via Navbar link or Home CTA.
2. Page renders a dedicated English program landing page.
3. Content includes: MCER level structure (A1–C2), schedule options (morning, evening, Saturday), diagnostic test offer, certification details.
4. `LeadForm` pre-selected with "Programa de Inglés".
5. User can submit the lead form (see `lead-submit-form` flow).

**Branching conditions:** None — dedicated static landing page.

---

## Lead Capture Module

### lead-submit-form

| Field | Value |
|-------|-------|
| **Priority** | P1 |
| **Roles** | visitor |
| **Frontend route** | `/`, `/:slug`, `/ingles` |
| **API endpoints** | `POST /api/contact/submit/` |

**Preconditions:** None.

**Steps:**

1. User sees the `LeadForm` component on any page (Home, program page, or English page).
2. Form displays fields: **Nombre** (name), **Correo** (email), **Teléfono** (phone), **Programa** (program selector).
3. If on a program page, the program selector is pre-filled with the current program name.
4. User fills in all required fields.
5. User clicks **Enviar** (submit) button.
6. Frontend shows loading state (spinner on button).
7. Frontend sends `POST /api/contact/submit/` with:
   ```json
   {
     "name": "Full Name",
     "email": "user@example.com",
     "phone": "+57 300 123 4567",
     "program": "Programa de Inglés",
     "captcha_token": ""
   }
   ```
8. Backend validates data via `ContactFormSerializer`.
9. Backend optionally verifies reCAPTCHA token (if `captcha_token` is non-empty and `RECAPTCHA_SECRET_KEY` is configured).
10. Backend sends notification email via `EmailService.send_contact_notification()`.
11. Backend returns `{ success: true, detail: "Mensaje enviado correctamente." }` (HTTP 200).
12. Frontend shows success state (checkmark icon + confirmation message).
13. Form resets for a new submission.

**Branching conditions:**

| Condition | Behavior |
|-----------|----------|
| Empty required fields | HTML `required` prevents submission |
| Invalid email format | Serializer returns `400 { success: false, errors: { email: [...] } }` |
| reCAPTCHA token provided but invalid | `400 { success: false, detail: "reCAPTCHA verification failed." }` |
| Email service failure | `500 { success: false, detail: "Error al enviar el mensaje. Intenta de nuevo." }` |
| No `RECAPTCHA_SECRET_KEY` configured | Captcha verification is skipped (development mode) |

---

### lead-whatsapp-cta

| Field | Value |
|-------|-------|
| **Priority** | P2 |
| **Roles** | visitor |
| **Frontend route** | all pages |
| **API endpoints** | None |

**Preconditions:** None.

**Steps:**

1. `WhatsAppButton` component renders as a floating button on every page (bottom-right).
2. User clicks the WhatsApp button.
3. Browser opens `https://wa.me/<phone-number>` with a pre-filled message in a new tab.
4. User continues the conversation in WhatsApp.

**Branching conditions:**

| Condition | Behavior |
|-----------|----------|
| Mobile device | Opens WhatsApp app directly |
| Desktop device | Opens WhatsApp Web in browser |

---

## Cross-Reference

| Artifact | Path | Purpose |
|----------|------|---------|
| Program Data | `frontend/src/app/data/programs.ts` | All program definitions (slug, name, icon, description, etc.) |
| Curriculum Data | `frontend/src/app/data/curriculum.ts` | Curriculum modules per program |
| API Client | `frontend/src/app/services/api.ts` | `submitContactForm()` function |
| Contact Serializer | `backend/base_feature_app/serializers/contact.py` | Lead form data validation |
| Contact View | `backend/base_feature_app/views/contact.py` | Lead form submission endpoint |
| Email Service | `backend/base_feature_app/services/email_service.py` | Notification email logic |
| Architecture Standard | `docs/DJANGO_REACT_ARCHITECTURE_STANDARD.md` | Generic architecture reference |

### Maintenance Rules

- **Adding a new flow:** Add entry here with full steps/branches, then create corresponding tests.
- **Modifying a flow:** Update steps and branches in this document first, then update tests accordingly.
- **Adding a new program:** Add to `frontend/src/app/data/programs.ts`. No flow map changes needed unless the page structure changes.
- **Bump `Version` and `Last Updated`** on every change.

# Frontend Rules — React 18 + Vite + TypeScript (Fernando Aragón)

## Stack

- **React 18.3.1** (not 19), **TypeScript 5.5**
- **Vite 7** as the dev server and bundler
- **react-router 7** with `createBrowserRouter` and a `Layout` route boundary
- **No state management library** — `useState` only
- **HTTP**: native `fetch` (no Axios), via `src/app/services/api.ts`
- **Tailwind CSS 4.1** + `@tailwindcss/vite`
- **shadcn/ui** components in `src/app/components/ui/` (~45 components)
- **Material UI 7.3** + `@emotion/react` / `@emotion/styled`
- **Radix UI** primitives (25+ packages, used by shadcn)
- **motion (Framer Motion) 12.23** for animations (`useInView` + `motion.div`)
- **lucide-react** for icons
- **react-hook-form 7.55** (installed but currently unused — the contact form uses `useState`)
- **react-day-picker 8.10** + **date-fns 3.6** for date pickers
- **swiper 12** + **embla-carousel-react** for carousels
- **recharts** for charts
- **next-themes** for dark mode
- **sonner** for toasts
- **Tests**: **Vitest 4.1** + React Testing Library 16.3 for unit; **Playwright 1.58** for E2E

This is a **React + Vite SPA** — **NOT Next.js**, **NOT Vue**, **NOT Nuxt**. There is no SSR, no `next.config.ts`, no App Router, no Server Components.

## Code Style and Structure

- **TypeScript-first**: every component is `.tsx`, every utility is `.ts`. Strict mode is on.
- Prefer **function components** with hooks. No class components.
- Use **named exports** for utilities and **default exports** for page components.
- Co-locate types with the component that uses them; promote to `src/app/types.ts` only when shared.
- Pages live in `src/app/pages/`, reusable components in `src/app/components/`, shadcn primitives in `src/app/components/ui/`.

## Naming Conventions

- **Component files**: PascalCase (`Layout.tsx`, `LeadForm.tsx`, `AnimatedCounter.tsx`, `Navbar.tsx`).
- **shadcn UI files**: kebab-case (`accordion.tsx`, `dialog.tsx`, `button.tsx`).
- **Pages**: PascalCase (`Home.tsx`, `English.tsx`, `ProgramPage.tsx`).
- **Utilities and services**: camelCase (`api.ts`, `utils.ts`).
- **Data modules**: camelCase (`programs.ts`, `curriculum.ts`).
- **Functions and state**: camelCase.

## Routing — react-router 7

- Routes are declared in `src/app/routes.ts` using `createBrowserRouter`.
- A root `Layout` route wraps everything and provides `Outlet` for child routes.
- Top-level routes:
  - `/` (Home) — Spanish landing
  - `/ingles` (English) — English landing (duplicated content)
  - `/:slug` (ProgramPage) — per-program detail page, parses slug from URL
- **Do not introduce file-based routing.** All routes are explicit in `routes.ts`.
- **Do not introduce Next.js App Router.**

## State Management — useState only

- The codebase has **no Zustand, no Redux, no Context API for global state**.
- All state is local `useState` inside components.
- If you find yourself needing to share state across more than 2-3 components, prefer lifting state to a parent or using `react-router`'s `loader`/`action` first. Only consider a global store if the user explicitly asks.

## HTTP — native fetch via `api.ts`

- All HTTP goes through `src/app/services/api.ts`.
- The current API surface is small: `submitContactForm(data: ContactFormData)`.
- Base URL: `import.meta.env.VITE_API_URL` (default `http://localhost:8000/api` in dev).
- **Do not introduce Axios** unless the user explicitly asks. Native `fetch` is sufficient for this codebase.

## Forms

- The current contact form (`LeadForm.tsx`) uses **local `useState`** + manual validation.
- `react-hook-form` is installed but **not used yet**. If you add a complex form, you may use it — but stay consistent within a given component.

## i18n — None (duplicated routes)

- There is **no i18n framework**. No `react-i18next`, no `next-intl`, no locale files.
- Spanish content lives at `/`, English at `/ingles`. Both are React components with content forked.
- If you need to update content in both languages, **edit both pages** (`Home.tsx` and `English.tsx`).
- Adding a third language would require a new route and content fork.

## UI Library Mix

This project uses **multiple UI libraries** in parallel:

| Library | Where used |
|---------|------------|
| **shadcn/ui** | `src/app/components/ui/` — 45+ pre-installed primitives (accordion, dialog, button, form, input, select, etc.) |
| **Material UI 7** | Some components via `@mui/material` |
| **Radix UI** | Underlies shadcn, also used directly for some primitives |
| **Tailwind CSS 4** | Utility classes everywhere, with the Vite plugin |

When adding a new component:
- Prefer **shadcn primitives** if one exists for what you need (it usually does).
- Fall back to Material UI only when shadcn lacks the component (rare).
- Always style with Tailwind utility classes — do not write separate CSS files.

## Animations — motion (Framer Motion)

- Use `motion.div`, `motion.section`, etc. from the `motion` package (which re-exports Framer Motion).
- Use `useInView` for scroll-triggered lazy animations.
- Common pattern:
  ```tsx
  <motion.section
    initial={{ opacity: 0, y: 20 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true }}
  >
  ```

## Testing — Vitest + Playwright

### Vitest (unit)
- Test files in `frontend/src/__tests__/` with `.test.tsx` or `.test.ts` extension.
- Run: `cd frontend && npm test -- path/to/file.test.tsx`
- Use **React Testing Library**: `render`, `screen`, `userEvent`. Prefer `screen.getByRole`, `screen.getByLabelText`, `screen.getByTestId`.
- Do not test implementation details — assert user-visible behavior.
- The `jsdom` environment is configured.

### Playwright (E2E)
- Specs in `frontend/e2e/`.
- Run: `cd frontend && npm run e2e -- path/to/spec.ts`
- Use `npm run e2e:headed` for debugging in a real browser; `npm run e2e:clean` to clear state.
- **Selector hierarchy**: `getByRole` > `getByTestId` > `locator('[data-testid=...]')`.
- **No `waitForTimeout()`** — use `toBeVisible()`, `waitForResponse()`, `waitForURL()`.
- **No `networkidle`** with Vite HMR — it never settles. Use `domcontentloaded` + element waits.

## Build → Django

- `npm run build` (Vite) emits to `backend/static/frontend/`.
- Django serves the SPA shell as a Django template that loads the Vite-hashed JS/CSS bundles.
- **Do not edit files inside `backend/static/frontend/`** — they are build artifacts.

## What NOT to do

- Do **not** introduce Next.js, App Router, Server Components, or any SSR layer.
- Do **not** introduce Zustand, Redux, or a global Context API for state.
- Do **not** introduce Axios — `fetch` is sufficient.
- Do **not** introduce an i18n framework — content is duplicated per route by design.
- Do **not** translate content client-side — edit both `Home.tsx` and `English.tsx` directly.
- Do **not** rewrite shadcn primitives in place — they are pre-generated and meant to be customized only when needed.

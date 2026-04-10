# Frontend Rules — Fernando Aragón

## Stack And Scope
- **React 18.3 + Vite 7 SPA + TypeScript 5.5** (NOT React 19, NOT Next.js, NOT Vue).
- **No state management library** — `useState` only.
- **HTTP**: native `fetch` via `src/app/services/api.ts` (no Axios).
- **Routing**: `react-router 7` with `createBrowserRouter` and a `Layout` boundary.
- **i18n**: none — Spanish at `/`, English at `/ingles` (duplicated routes).
- **Styling**: Tailwind CSS 4 + `@tailwindcss/vite` plugin.
- **UI library mix**: shadcn/ui (45+ primitives in `src/app/components/ui/`) + Material UI 7 + Radix UI underneath.
- **Animations**: `motion` (Framer Motion) with `useInView`.
- **Tests**: Vitest 4.1 + React Testing Library for unit; Playwright 1.58 for E2E.

## Project Conventions
- **TypeScript-first**. Components are `.tsx`, utilities `.ts`. Strict mode is on.
- Function components with hooks. No class components.
- **No Zustand, no Redux, no global Context** — `useState` is enough for this codebase.
- **No Axios** — native `fetch` via the single `api.ts` helper.
- **No i18n framework** — content is forked between `Home.tsx` (Spanish) and `English.tsx` (English). Updating bilingual content means editing both pages.
- **Filename conventions**:
  - Component files → PascalCase (`LeadForm.tsx`, `Layout.tsx`).
  - shadcn UI files → kebab-case (`accordion.tsx`, `button.tsx`).
  - Pages → PascalCase (`Home.tsx`, `English.tsx`, `ProgramPage.tsx`).
  - Utilities, services, data → camelCase (`api.ts`, `programs.ts`, `curriculum.ts`).
- **UI library priority**: prefer shadcn primitives when one exists; fall back to Material UI only when shadcn lacks the component.

## UX And Routing
- Routes are explicit in `src/app/routes.ts` using `createBrowserRouter`. Do not introduce file-based routing.
- Top-level routes: `/` (Home), `/ingles` (English), `/:slug` (ProgramPage).
- For Playwright and async UI work, prefer **role-based locators** and **explicit element waits**.
- Do **not** use `networkidle` for Vite flows — the HMR WebSocket prevents it from settling.

## Commands
- Dev server: `cd frontend && npm run dev` (Vite, default :5173)
- Unit tests (Vitest): `cd frontend && npm test -- path/to/file.test.tsx`
- E2E (Playwright): `cd frontend && npm run e2e -- path/to/spec.ts` (or `e2e:headed` / `e2e:clean`)
- Build: `cd frontend && npm run build` (emits to `../backend/static/frontend/`)

## Testing Rules
- Never run the full frontend unit or E2E suite.
- Maximum 20 tests per batch and 3 commands per cycle.
- Assert user-visible behavior, not implementation details.
- Use stable locators in E2E (`getByRole` > `getByTestId`).

# Vulnerability Audit & Dependency Update Report

**Branch**: `double-check-30042026`
**Date**: 2026-04-30
**Project**: fernando_aragon_project

## Summary CVEs by Severity

### Frontend (npm)
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 3 |
| Moderate | 3 |
| Low | 0 |
| **Total** | **6** |

Affected packages: `vite`, `lodash`, `picomatch`, `postcss`, `yaml`, `brace-expansion`.

### Backend (pip)
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High/Moderate (CVSS) | 11 |
| **Total advisories** | **11** |

Affected packages: `Django` (7 advisories), `python-dotenv` (1), `pillow` (1), `pytest` (1), `requests` (1).

## Outdated Tables

### Frontend (patch+minor targets)
| Package | Current | Target (minor) | Latest |
|---------|---------|----------------|--------|
| @playwright/test | 1.58.2 | 1.59.1 | 1.59.1 |
| @types/node | 25.5.0 | 25.6.0 | 25.6.0 |
| @vitest/coverage-v8 | 4.1.0 | 4.1.5 | 4.1.5 |
| jsdom | 29.0.0 | 29.1.1 | 29.1.1 |
| swiper | 12.1.3 | 12.1.4 | 12.1.4 |
| typescript-eslint | 8.57.1 | 8.59.1 | 8.59.1 |
| vite | 7.3.1 | 7.3.2 | 8.0.10 |
| vitest | 4.1.0 | 4.1.5 | 4.1.5 |
| @radix-ui/react-* (many) | various | latest within major 1.x/2.x | unchanged majors |
| @tailwindcss/vite | 4.1.12 | 4.2.4 | 4.2.4 |
| tailwindcss | 4.1.12 | 4.2.4 | 4.2.4 |
| react-router | 7.13.0 | 7.14.2 | 7.14.2 |
| react-hook-form | 7.55.0 | 7.74.0 | 7.74.0 |
| sonner | 2.0.3 | 2.0.7 | 2.0.7 |
| motion | 12.23.24 | 12.38.0 | 12.38.0 |
| tailwind-merge | 3.2.0 | 3.5.0 | 3.5.0 |
| tw-animate-css | 1.3.8 | 1.4.0 | 1.4.0 |
| @vitejs/plugin-react | 5.2.0 | 5.2.0 | 6.0.1 |

### Backend (patch+minor targets)
| Package | Current | Target | Latest |
|---------|---------|--------|--------|
| coverage | 7.13.4 | 7.13.5 | 7.13.5 |
| Django | 6.0.2 | 6.0.4 | 6.0.4 |
| djangorestframework | 3.16.1 | 3.17.1 | 3.17.1 |
| Faker | 40.5.1 | 40.15.0 | 40.15.0 |
| pillow | 12.1.1 | 12.2.0 | 12.2.0 |
| pytest | 9.0.2 | 9.0.3 | 9.0.3 |
| pytest-cov | 7.0.0 | 7.1.0 | 7.1.0 |
| python-dotenv | 1.2.1 | 1.2.2 | 1.2.2 |
| requests | 2.32.5 | 2.33.1 | 2.33.1 |
| ruff | 0.15.2 | 0.15.12 | 0.15.12 |

## CVE Details

### Frontend
- **vite (high)** GHSA-p9ff-h696-f583 — Arbitrary File Read via WebSocket (range 7.0.0 – 7.3.1).
- **vite (high)** GHSA-v2wj-q39q-566r — `server.fs.deny` bypassed with queries (7.1.0 – 7.3.1).
- **vite (moderate)** GHSA-4w7w-66w2-5vf9 — Path traversal in optimized deps `.map` (7.0.0 – 7.3.1). Fix: vite >= 7.3.2.
- **lodash (high)** GHSA-r5fr-rjxr-66jc — Code injection via `_.template` (transitive).
- **lodash (moderate)** GHSA-f23m-r3pf-42rh — Prototype pollution in `_.unset` / `_.omit`.
- **picomatch (high)** GHSA-c2c7-rcm5-vvqj — ReDoS via extglob quantifiers (4.0.0 – 4.0.3).
- **picomatch (moderate)** GHSA-3v7f-55p6-f55p — Method injection in POSIX classes.
- **postcss (moderate)** GHSA-qx2v-qp2m-jg93 — XSS via unescaped `</style>` in stringify output.
- **yaml (moderate)** GHSA-48c2-rrv3-qjmp — Stack overflow via deep nesting.
- **brace-expansion (moderate)** GHSA-f886-m6hf-6m8v — DoS via zero-step sequence.

### Backend
- **Django** CVE-2026-25674 (GHSA-mjgh-79qc-68w3) — race condition in file-system storage and file-based cache. Fix: 6.0.3.
- **Django** CVE-2026-25673 (GHSA-8p8v-wh79-9r56) — `URLField.to_python()` ReDoS. Fix: 6.0.3.
- **Django** CVE-2026-33033 (GHSA-5mf9-h53q-7mhq) — `MultiPartParser` performance DoS via base64 whitespace. Fix: 6.0.4.
- **Django** CVE-2026-33034 (GHSA-933h-hp56-hf7m) — ASGI bypass of `DATA_UPLOAD_MAX_MEMORY_SIZE`. Fix: 6.0.4.
- **Django** CVE-2026-4292 (GHSA-mmwr-2jhp-mc7j) — `ModelAdmin.list_editable` forged POST creates instances. Fix: 6.0.4.
- **Django** CVE-2026-4277 (GHSA-pwjp-ccjc-ghwg) — Add permissions on `GenericInlineModelAdmin` not validated. Fix: 6.0.4.
- **Django** CVE-2026-3902 (GHSA-mvfq-ggxm-9mc5) — `ASGIRequest` header spoofing via hyphen/underscore variant ambiguity. Fix: 6.0.4.
- **python-dotenv** CVE-2026-28684 (GHSA-mf9w-mj56-hr94) — `set_key`/`unset_key` follow symlinks across devices, arbitrary file overwrite. Fix: 1.2.2.
- **pillow** CVE-2026-40192 (GHSA-whj4-6x5x-4v2j) — FITS GZIP decompression bomb (DoS). Fix: 12.2.0.
- **pytest** CVE-2025-71176 (GHSA-6w46-j5rx-g56g) — predictable `/tmp/pytest-of-{user}` directory; local DoS / privilege issues. Fix: 9.0.3.
- **requests** CVE-2026-25645 (GHSA-gc5v-m9x4-r6x2) — `extract_zipped_paths()` predictable temp filename. Fix: 2.33.0. Standard usage of requests is not affected; only direct use of `extract_zipped_paths()`.

## Reproducibility Commands

### Frontend
```bash
cd frontend
npm install
npm audit --json > /tmp/fernando_aragon_project-npm-audit.json
npm outdated --json > /tmp/fernando_aragon_project-npm-outdated.json
```

### Backend
```bash
cd backend
python3 -m venv .venv-audit
.venv-audit/bin/pip install --upgrade pip pip-audit
.venv-audit/bin/pip install -r requirements.txt
.venv-audit/bin/pip-audit -r requirements.txt --format json > /tmp/fernando_aragon_project-pip-audit.json
.venv-audit/bin/pip list --outdated --format json > /tmp/fernando_aragon_project-pip-outdated.json
```

## Majors Skipped (per policy, no major bumps)

### Frontend
- `@eslint/js` 9.x → 10.x
- `@mui/icons-material` 7 → 9
- `@mui/material` 7 → 9
- `@vitejs/plugin-react` 5 → 6
- `date-fns` 3 → 4
- `eslint` 9 → 10
- `lucide-react` 0.487 → 1.x
- `react` / `react-dom` 18 → 19
- `@types/react` / `@types/react-dom` 18 → 19
- `react-day-picker` 8 → 9
- `react-resizable-panels` 2 → 4
- `recharts` 2 → 3
- `typescript` 5 → 6
- `vite` 7 → 8

### Backend
- None pending major bumps in this scan window beyond what was already at latest major.

## Updates Applied

(To be filled in after Section D — apply patch+minor updates.)

## Build / Tests / Rollbacks

(To be filled in after Section E — verification.)

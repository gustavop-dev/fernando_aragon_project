---
trigger: model_decision
description: Coverage report configuration for pytest (backend) and Vitest (frontend). Use when setting up coverage, modifying conftest.py coverage hooks, configuring Vitest coverage reporters, or interpreting coverage output.
---

# Backend & Frontend Coverage Report Standard

Full reference: `docs/BACKEND_AND_FRONTEND_COVERAGE_REPORT_STANDARD.md`

## Shared Color Thresholds

| Coverage % | Color | Meaning |
|------------|-------|---------|
| > 80% | 🟢 Green | Good |
| 50–80% | 🟡 Yellow | Needs improvement |
| < 50% | 🔴 Red | Critical — prioritize |

## Backend — pytest Coverage

### Dependencies

`pytest`, `pytest-cov`, `pytest-django`, `coverage` — all in `backend/requirements.txt`.

### Config: `backend/pytest.ini`

```ini
[pytest]
DJANGO_SETTINGS_MODULE = base_feature_project.settings
python_files = test_*.py tests.py
testpaths =
    base_feature_app/tests
    django_attachments
norecursedirs =
    venv
addopts = -ra --cov=base_feature_app --cov-report=
```

### Custom Reporter: `backend/conftest.py`

The `conftest.py` contains 3 pytest hooks that:
1. **Suppress** default `pytest-cov` terminal report
2. **Read** `.coverage` data file directly
3. **Render** custom colored table with per-file stats + focus footer

**Adaptation points when modifying:**
- App name filter: search for the app name string in `conftest.py` (filters source files, excludes `/tests/`)
- Top-N focus count: the `[:3]` slice controls how many low-coverage files appear in the footer
- Bar widths: `_MINI_W` (per-file) and `_WIDE_W` (total row)

### Run Command

```bash
source venv/bin/activate && pytest --cov
```

### Report Sections

1. **Per-file table**: path | stmts | missing | pct% | [bar]
2. **TOTAL summary row**
3. **Focus footer**: "Top-N files to focus on" or "All files fully covered"

---

## Frontend — Vitest Coverage

### Config: `frontend/vitest.config.ts`

Key settings:
```ts
coverage: {
  provider: 'v8',
  reporter: ['text', 'text-summary', 'json-summary'],
  include: ['src/app/**/*.{ts,tsx}'],
  exclude: ['src/app/components/ui/**', 'src/**/*.{test,spec}.{ts,tsx}', 'src/__tests__/**'],
}
```
- `text` → per-file table
- `text-summary` → Statements/Branches/Functions/Lines totals
- `json-summary` → writes `coverage/coverage-summary.json`

### Run Command

```bash
npm run test:coverage
```

This runs: `vitest run --coverage`

### Report Sections (2 in sequence)

1. **Vitest `text` reporter**: per-file table (Stmts/Branch/Funcs/Lines)
2. **Vitest `text-summary`**: Coverage summary block

---

## Interpreting Coverage Output

- **Prioritize** files with lowest % and highest "Miss" count
- **Priority order**: Views → Serializers → Models → Utils → Tasks (backend); Stores → Composables → Components (frontend)
- **Do not** polish near-100% files until low-coverage files are addressed
- Coverage measures lines executed, **not** behavior verified — a test with no assertions gives coverage but no value

"""
Combine coverage reports from backend, frontend-unit, and frontend-e2e
into a unified Markdown summary for GitHub Actions Job Summary.

Reads:
  - backend-coverage-report/backend-coverage.json   (coverage.py JSON format)
  - frontend-unit-coverage-report/coverage-summary.json (vitest json-summary)
  - frontend-e2e-coverage-report/flow-coverage.json (custom Playwright reporter)

Writes:
  - coverage-summary.md  (artifact)
  - $GITHUB_STEP_SUMMARY (if running in GH Actions)
"""

from __future__ import annotations

import json
import os
from pathlib import Path

BAR_WIDTH = 20


def _read_json(path: Path) -> dict | None:
    if not path.exists():
        print(f"⚠️  Not found: {path}")
        return None
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _pct_emoji(pct: float) -> str:
    if pct >= 90:
        return "🟢"
    if pct >= 70:
        return "🟡"
    return "🔴"


def _status_emoji(status: str) -> str:
    return {
        "covered": "✅",
        "partial": "⚠️",
        "failing": "❌",
        "missing": "⬜",
    }.get(status, "❓")


def _bar(pct: float, width: int = BAR_WIDTH) -> str:
    filled = round(pct / 100 * width)
    empty = width - filled
    return "█" * filled + "░" * empty


# ── Section builders ─────────────────────────────────────────────────
# Each returns (table_row: str, details: list[str])


def build_backend_section(data: dict | None) -> tuple[str, list[str]]:
    details: list[str] = []

    if data is None:
        return "| Backend (pytest) | — | — | — | — | ⚠️ No report |", details

    totals = data.get("totals", {})
    stmts_pct = totals.get("percent_covered", 0.0)
    num_stmts = totals.get("num_statements", 0)
    missing = totals.get("missing_lines", 0)
    branches_pct = 0.0
    num_branches = totals.get("num_branches", 0)
    missing_branches = totals.get("missing_branches", 0)
    if num_branches > 0:
        branches_pct = ((num_branches - missing_branches) / num_branches) * 100

    emoji = _pct_emoji(stmts_pct)
    row = (
        f"| Backend (pytest) | {stmts_pct:.1f}% | "
        f"{branches_pct:.1f}% | {num_stmts} | {missing} | {emoji} |"
    )

    # Top uncovered files
    files_data = data.get("files", {})
    uncovered = []
    for fpath, info in files_data.items():
        summary = info.get("summary", {})
        file_stmts = summary.get("num_statements", 0)
        file_missing = summary.get("missing_lines", 0)
        file_pct = summary.get("percent_covered", 100.0)
        if file_missing > 0:
            short = fpath.split("base_feature_app/")[-1] if "base_feature_app/" in fpath else fpath
            uncovered.append((short, file_stmts, file_missing, file_pct))

    if uncovered:
        uncovered.sort(key=lambda x: x[3])
        details.append("")
        details.append("<details><summary>📋 Backend — Top uncovered files</summary>")
        details.append("")
        details.append("| File | Stmts | Miss | Cover | Bar |")
        details.append("|------|------:|-----:|------:|-----|")
        for name, stmts, miss, pct in uncovered[:10]:
            details.append(
                f"| `{name}` | {stmts} | {miss} | {pct:.1f}% | `{_bar(pct)}` |"
            )
        details.append("")
        details.append("</details>")

    return row, details


def build_frontend_unit_section(data: dict | None) -> tuple[str, list[str]]:
    details: list[str] = []

    if data is None:
        return "| Frontend Unit (vitest) | — | — | — | — | ⚠️ No report |", details

    total = data.get("total", {})
    stmts = total.get("statements", {})
    branches = total.get("branches", {})

    stmts_pct = stmts.get("pct", 0)
    branches_pct = branches.get("pct", 0)
    stmts_total = stmts.get("total", 0)
    stmts_missing = stmts_total - stmts.get("covered", 0)

    emoji = _pct_emoji(stmts_pct)
    row = (
        f"| Frontend Unit (vitest) | {stmts_pct:.1f}% | "
        f"{branches_pct:.1f}% | {stmts_total} | {stmts_missing} | {emoji} |"
    )

    # Top uncovered files
    uncovered = []
    for fpath, info in data.items():
        if fpath == "total":
            continue
        file_stmts = info.get("statements", {})
        file_total = file_stmts.get("total", 0)
        file_covered = file_stmts.get("covered", 0)
        file_missing = file_total - file_covered
        file_pct = file_stmts.get("pct", 100)
        if file_missing > 0:
            short = fpath.split("/src/")[-1] if "/src/" in fpath else fpath
            uncovered.append((short, file_total, file_missing, file_pct))

    if uncovered:
        uncovered.sort(key=lambda x: x[3])
        details.append("")
        details.append("<details><summary>📋 Frontend Unit — Top uncovered files</summary>")
        details.append("")
        details.append("| File | Stmts | Miss | Cover | Bar |")
        details.append("|------|------:|-----:|------:|-----|")
        for name, stmts_t, miss, pct in uncovered[:10]:
            details.append(
                f"| `{name}` | {stmts_t} | {miss} | {pct:.1f}% | `{_bar(pct)}` |"
            )
        details.append("")
        details.append("</details>")

    return row, details


def build_e2e_section(data: dict | None) -> tuple[str, list[str]]:
    details: list[str] = []

    if data is None:
        return "| Frontend E2E (Playwright) | — | — | — | — | ⚠️ No report |", details

    summary = data.get("summary", {})
    total_flows = summary.get("total", 0)
    covered = summary.get("covered", 0)
    failing = summary.get("failing", 0)
    missing = summary.get("missing", 0)

    pct = (covered / total_flows * 100) if total_flows > 0 else 0
    emoji = _pct_emoji(pct)

    row = (
        f"| Frontend E2E (Playwright) | {pct:.1f}% flows | "
        f"{covered}/{total_flows} covered | "
        f"{failing} failing | {missing} missing | {emoji} |"
    )

    # Detail: missing/failing flows
    flows = data.get("flows", {})
    problem_flows = []
    for flow_id, flow_data in flows.items():
        status = flow_data.get("status", "missing")
        if status in ("missing", "failing"):
            priority = flow_data.get("definition", {}).get("priority", "P4")
            name = flow_data.get("definition", {}).get("name", flow_id)
            problem_flows.append((flow_id, name, status, priority))

    if problem_flows:
        problem_flows.sort(key=lambda x: x[3])
        details.append("")
        details.append("<details><summary>📋 E2E — Missing/Failing flows</summary>")
        details.append("")
        details.append("| Flow ID | Name | Status | Priority |")
        details.append("|---------|------|--------|----------|")
        for fid, name, status, priority in problem_flows[:15]:
            details.append(
                f"| `{fid}` | {name} | {_status_emoji(status)} {status} | {priority} |"
            )
        details.append("")
        details.append("</details>")

    return row, details


def main() -> None:
    reports_dir = Path(os.getenv("REPORTS_DIR", "."))

    backend_data = _read_json(reports_dir / "backend-coverage-report" / "backend-coverage.json")
    frontend_unit_data = _read_json(
        reports_dir / "frontend-unit-coverage-report" / "coverage-summary.json"
    )
    e2e_data = _read_json(reports_dir / "frontend-e2e-coverage-report" / "flow-coverage.json")

    # Build sections — each returns (table_row, details_lines)
    backend_row, backend_details = build_backend_section(backend_data)
    frontend_row, frontend_details = build_frontend_unit_section(frontend_unit_data)
    e2e_row, e2e_details = build_e2e_section(e2e_data)

    md: list[str] = []

    # ── Title ──
    md.append("# 📊 Coverage Summary")
    md.append("")

    # ── Summary table (no details mixed in) ──
    md.append("## Overview")
    md.append("")
    md.append("| Suite | Stmts | Branches | Total | Missing | Status |")
    md.append("|-------|------:|---------:|------:|--------:|--------|")
    md.append(backend_row)
    md.append(frontend_row)
    md.append(e2e_row)
    md.append("")

    # ── Overall status ──
    all_ok = True
    suites_found = 0
    if backend_data:
        suites_found += 1
        if backend_data.get("totals", {}).get("percent_covered", 0) < 70:
            all_ok = False
    if frontend_unit_data:
        suites_found += 1
        if frontend_unit_data.get("total", {}).get("statements", {}).get("pct", 0) < 70:
            all_ok = False
    if e2e_data:
        suites_found += 1
        e2e_summary = e2e_data.get("summary", {})
        if e2e_summary.get("failing", 0) > 0:
            all_ok = False

    if suites_found == 0:
        md.append("> ⚠️ No coverage reports found. Check that the test jobs completed successfully.")
    elif all_ok:
        md.append("> ✅ All suites meet minimum coverage thresholds.")
    else:
        md.append("> ⚠️ Some suites are below recommended thresholds or have failing tests.")

    md.append("")

    # ── Detail sections (after the table) ──
    has_details = backend_details or frontend_details or e2e_details
    if has_details:
        md.append("---")
        md.append("")
        md.append("## Details")
        md.extend(backend_details)
        md.extend(frontend_details)
        md.extend(e2e_details)
        md.append("")

    md.append("---")
    md.append(f"*Generated by CI — {suites_found}/3 suites reported*")

    report_text = "\n".join(md)

    # Write artifact
    output_path = reports_dir / "coverage-summary.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report_text, encoding="utf-8")
    print(f"✅ Report written to {output_path}")

    # Write to GitHub Step Summary if in Actions
    summary_path = os.getenv("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as fh:
            fh.write(report_text)
            fh.write("\n")
        print("✅ Report appended to $GITHUB_STEP_SUMMARY")

    # Print to stdout as well
    print("\n" + report_text)


if __name__ == "__main__":
    main()

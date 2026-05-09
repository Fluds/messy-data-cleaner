# AGENT_BRIEF

## Product Goal

Messy Data Cleaner should be a small, reliable public demo that helps people upload CSV or Excel files, identify common data quality issues, apply conservative cleanup steps, and download cleaned data plus a simple report.

## Current Scope

- Streamlit single-page app
- CSV, XLSX, and XLS upload
- First-row preview
- Detection for:
  - empty rows
  - empty columns
  - duplicate rows
  - missing values and missing percentages by column
  - leading or trailing spaces in column names
  - constant columns
- Optional cleaning for:
  - stripping column-name whitespace
  - removing fully empty rows
  - removing fully empty columns
  - removing duplicate rows
- Downloads for:
  - cleaned CSV
  - cleaned XLSX
  - HTML data quality report
- Included sample data in `examples/`
- Basic pytest coverage for core cleaning logic

## Constraints

- No database
- No login or account system
- No external APIs
- No secrets or API keys
- No complex AI features
- No heavy architecture
- Keep code easy to read and maintain
- Prefer boring reliability over fancy features

## Next-Step Protocol For Future Codex Tasks

1. Inspect the current repo state before editing.
2. Run or update focused tests for the behavior being changed.
3. Keep changes small and demo-oriented.
4. Preserve the simple Streamlit structure unless there is a clear reason to refactor.
5. Avoid adding dependencies unless they solve a real problem and are easy to justify.
6. Update README or this brief when product behavior or scope changes.
7. Verify with `pytest` and a Streamlit startup smoke check when practical.

## Improvement Rule

Prefer small, shippable improvements over broad rewrites.

from __future__ import annotations

from html import escape
from typing import Any

import pandas as pd


def _render_list(items: list[str]) -> str:
    if not items:
        return "<p>None detected.</p>"
    rows = "".join(f"<li>{escape(item)}</li>" for item in items)
    return f"<ul>{rows}</ul>"


def _render_missing_values(missing_values: dict[str, int]) -> str:
    if not missing_values:
        return "<p>No missing values detected.</p>"

    rows = "".join(
        "<tr>"
        f"<td>{escape(column)}</td>"
        f"<td>{count}</td>"
        "</tr>"
        for column, count in missing_values.items()
    )
    return f"""
    <table>
        <thead><tr><th>Column</th><th>Missing values</th></tr></thead>
        <tbody>{rows}</tbody>
    </table>
    """


def generate_html_report(
    original_df: pd.DataFrame,
    cleaned_df: pd.DataFrame,
    issues: dict[str, Any],
    applied_steps: list[str],
) -> str:
    before_rows, before_columns = original_df.shape
    after_rows, after_columns = cleaned_df.shape

    return f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Messy Data Cleaner Report</title>
    <style>
        :root {{
            color-scheme: light;
            --ink: #17202a;
            --muted: #5d6d7e;
            --line: #d7dbdd;
            --panel: #f7f9fb;
            --accent: #1f7a8c;
        }}
        body {{
            margin: 0;
            font-family: Inter, Segoe UI, Arial, sans-serif;
            color: var(--ink);
            background: #ffffff;
            line-height: 1.5;
        }}
        main {{
            max-width: 920px;
            margin: 0 auto;
            padding: 32px 24px 48px;
        }}
        h1, h2 {{
            line-height: 1.2;
        }}
        h1 {{
            margin-bottom: 4px;
        }}
        h2 {{
            margin-top: 28px;
            border-bottom: 1px solid var(--line);
            padding-bottom: 8px;
        }}
        .subtitle {{
            margin-top: 0;
            color: var(--muted);
        }}
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 12px;
            margin: 24px 0;
        }}
        .metric {{
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 14px;
        }}
        .metric strong {{
            display: block;
            font-size: 1.4rem;
            color: var(--accent);
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin-top: 12px;
        }}
        th, td {{
            border: 1px solid var(--line);
            padding: 8px 10px;
            text-align: left;
        }}
        th {{
            background: var(--panel);
        }}
        ul {{
            padding-left: 22px;
        }}
    </style>
</head>
<body>
<main>
    <h1>Messy Data Cleaner Report</h1>
    <p class="subtitle">A concise data quality summary for the uploaded file.</p>

    <section class="metrics">
        <div class="metric"><span>Original shape</span><strong>{before_rows} x {before_columns}</strong></div>
        <div class="metric"><span>Cleaned shape</span><strong>{after_rows} x {after_columns}</strong></div>
        <div class="metric"><span>Duplicate rows</span><strong>{issues["duplicate_rows"]}</strong></div>
        <div class="metric"><span>Empty rows</span><strong>{issues["empty_rows"]}</strong></div>
    </section>

    <h2>Detected Issues</h2>
    <p><strong>Empty columns:</strong></p>
    {_render_list(issues["empty_columns"])}
    <p><strong>Suspicious column names:</strong></p>
    {_render_list(issues["suspicious_column_names"])}
    <p><strong>Constant columns:</strong></p>
    {_render_list(issues["constant_columns"])}

    <h2>Missing Value Summary</h2>
    {_render_missing_values(issues["missing_values"])}

    <h2>Applied Cleaning Steps</h2>
    {_render_list(applied_steps)}
</main>
</body>
</html>
"""

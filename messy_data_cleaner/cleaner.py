from dataclasses import dataclass
from typing import Any

import pandas as pd


@dataclass(frozen=True)
class CleaningOptions:
    strip_column_names: bool = True
    remove_empty_rows: bool = True
    remove_empty_columns: bool = True
    remove_duplicate_rows: bool = True


def analyze_dataframe(df: pd.DataFrame) -> dict[str, Any]:
    """Return a small, serializable summary of common data quality issues."""
    row_count = len(df)
    empty_rows = int(df.isna().all(axis=1).sum())
    empty_columns = [str(column) for column in df.columns[df.isna().all(axis=0)]]
    duplicate_rows = int(df.duplicated().sum())
    missing_values = {
        str(column): int(count)
        for column, count in df.isna().sum().items()
        if int(count) > 0
    }
    missing_percentages = {
        column: round((count / row_count) * 100, 1) if row_count else 0.0
        for column, count in missing_values.items()
    }
    suspicious_column_names = [
        str(column) for column in df.columns if str(column) != str(column).strip()
    ]
    constant_columns = [
        str(column) for column in df.columns if df[column].dropna().nunique() <= 1
    ]

    return {
        "shape": tuple(df.shape),
        "empty_rows": empty_rows,
        "empty_columns": empty_columns,
        "duplicate_rows": duplicate_rows,
        "missing_values": missing_values,
        "missing_percentages": missing_percentages,
        "suspicious_column_names": suspicious_column_names,
        "constant_columns": constant_columns,
    }


def summarize_issues(issues: dict[str, Any]) -> dict[str, Any]:
    """Build a short user-facing issue summary for the app and reports."""
    issue_counts = {
        "empty row(s)": issues["empty_rows"],
        "empty column(s)": len(issues["empty_columns"]),
        "duplicate row(s)": issues["duplicate_rows"],
        "column(s) with missing values": len(issues["missing_values"]),
        "suspicious column name(s)": len(issues["suspicious_column_names"]),
        "constant column(s)": len(issues["constant_columns"]),
    }
    active_issues = {
        label: count for label, count in issue_counts.items() if int(count) > 0
    }

    if not active_issues:
        return {
            "count": 0,
            "headline": "No major issues found",
            "details": "The uploaded file looks clean based on the checks this app runs.",
        }

    details = ", ".join(f"{count} {label}" for label, count in active_issues.items())
    return {
        "count": sum(int(count) for count in active_issues.values()),
        "headline": "Data quality issues found",
        "details": details,
    }


def clean_dataframe(
    df: pd.DataFrame,
    options: CleaningOptions | None = None,
) -> tuple[pd.DataFrame, list[str]]:
    """Apply selected cleaning steps and return the cleaned frame plus step labels."""
    options = options or CleaningOptions()
    cleaned = df.copy()
    applied_steps: list[str] = []

    if options.strip_column_names:
        stripped_columns = [str(column).strip() for column in cleaned.columns]
        if list(cleaned.columns) != stripped_columns:
            cleaned.columns = stripped_columns
            applied_steps.append("Stripped whitespace from column names")

    if options.remove_empty_rows:
        before = len(cleaned)
        cleaned = cleaned.dropna(axis=0, how="all")
        removed = before - len(cleaned)
        if removed:
            applied_steps.append(f"Removed {removed} fully empty row(s)")

    if options.remove_empty_columns:
        before = len(cleaned.columns)
        cleaned = cleaned.dropna(axis=1, how="all")
        removed = before - len(cleaned.columns)
        if removed:
            applied_steps.append(f"Removed {removed} fully empty column(s)")

    if options.remove_duplicate_rows:
        before = len(cleaned)
        cleaned = cleaned.drop_duplicates()
        removed = before - len(cleaned)
        if removed:
            applied_steps.append(f"Removed {removed} duplicate row(s)")

    if not applied_steps:
        applied_steps.append("No cleaning steps changed the data")

    return cleaned, applied_steps

import pandas as pd

from messy_data_cleaner.cleaner import CleaningOptions, analyze_dataframe, clean_dataframe


def messy_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            " Name ": ["Ada", "Grace", "Grace", None],
            "Department": ["Analytics", "Engineering", "Engineering", None],
            "Empty": [None, None, None, None],
            "Status": ["active", "active", "active", None],
        }
    )


def test_analyze_dataframe_detects_common_issues() -> None:
    issues = analyze_dataframe(messy_frame())

    assert issues["shape"] == (4, 4)
    assert issues["empty_rows"] == 1
    assert issues["empty_columns"] == ["Empty"]
    assert issues["duplicate_rows"] == 1
    assert issues["missing_values"] == {
        " Name ": 1,
        "Department": 1,
        "Empty": 4,
        "Status": 1,
    }
    assert issues["suspicious_column_names"] == [" Name "]
    assert set(issues["constant_columns"]) == {"Empty", "Status"}


def test_clean_dataframe_applies_selected_options() -> None:
    cleaned, steps = clean_dataframe(messy_frame())

    assert cleaned.shape == (2, 3)
    assert list(cleaned.columns) == ["Name", "Department", "Status"]
    assert "Stripped whitespace from column names" in steps
    assert "Removed 1 fully empty row(s)" in steps
    assert "Removed 1 fully empty column(s)" in steps
    assert "Removed 1 duplicate row(s)" in steps


def test_clean_dataframe_respects_disabled_options() -> None:
    cleaned, steps = clean_dataframe(
        messy_frame(),
        CleaningOptions(
            strip_column_names=False,
            remove_empty_rows=False,
            remove_empty_columns=False,
            remove_duplicate_rows=False,
        ),
    )

    assert cleaned.shape == (4, 4)
    assert list(cleaned.columns) == [" Name ", "Department", "Empty", "Status"]
    assert steps == ["No cleaning steps changed the data"]

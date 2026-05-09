import pandas as pd

from messy_data_cleaner.cleaner import analyze_dataframe, clean_dataframe, summarize_issues
from messy_data_cleaner.report import generate_html_report


def test_generate_html_report_contains_expected_sections() -> None:
    original_df = pd.DataFrame(
        {
            "Name": ["Ada", None],
            "Score": [91, None],
        }
    )
    cleaned_df, applied_steps = clean_dataframe(original_df)
    issues = analyze_dataframe(original_df)
    issues["summary"] = summarize_issues(issues)

    html = generate_html_report(original_df, cleaned_df, issues, applied_steps)

    assert "<html" in html
    assert "Messy Data Cleaner Report" in html
    assert "Missing Value Summary" in html
    assert "Applied Cleaning Steps" in html

from io import BytesIO
from pathlib import Path

import pandas as pd
import streamlit as st

from messy_data_cleaner import (
    CleaningOptions,
    analyze_dataframe,
    clean_dataframe,
    summarize_issues,
)
from messy_data_cleaner.report import generate_html_report


st.set_page_config(page_title="Messy Data Cleaner", layout="wide")

SAMPLE_FILE = Path("examples/messy_sample.csv")


@st.cache_data(show_spinner=False)
def load_uploaded_file(file_name: str, file_bytes: bytes) -> pd.DataFrame:
    buffer = BytesIO(file_bytes)
    if file_name.lower().endswith(".csv"):
        return pd.read_csv(buffer)
    if file_name.lower().endswith((".xlsx", ".xls")):
        return pd.read_excel(buffer)
    raise ValueError("Unsupported file type. Please upload a CSV or Excel file.")


def csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def xlsx_bytes(df: pd.DataFrame) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Cleaned Data")
    return output.getvalue()


def load_sample_file() -> tuple[str, bytes] | None:
    if not SAMPLE_FILE.exists():
        return None
    return SAMPLE_FILE.name, SAMPLE_FILE.read_bytes()


st.title("Messy Data Cleaner")
st.caption("Upload a CSV or Excel file, review common quality issues, and download a cleaned file plus a simple HTML report.")

with st.expander("Try it with sample data", expanded=True):
    st.write("Use the included messy sample to see the checks and downloads without preparing a file first.")
    sample_file = load_sample_file()
    if sample_file is None:
        st.warning("Sample data is not available in this deployment. Upload your own CSV or Excel file to continue.")
    else:
        sample_name, sample_bytes = sample_file
        sample_columns = st.columns(2)
        if sample_columns[0].button("Use sample data", use_container_width=True):
            st.session_state["sample_data"] = {
                "name": sample_name,
                "bytes": sample_bytes,
            }
        sample_columns[1].download_button(
            "Download sample CSV",
            data=sample_bytes,
            file_name=sample_name,
            mime="text/csv",
            use_container_width=True,
        )

uploaded_file = st.file_uploader("Upload CSV or XLSX", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    file_name = uploaded_file.name
    file_bytes = uploaded_file.getvalue()
elif "sample_data" in st.session_state:
    file_name = st.session_state["sample_data"]["name"]
    file_bytes = st.session_state["sample_data"]["bytes"]
    st.info(f"Using sample file: `{file_name}`")
else:
    st.info("Upload your own file or use the sample data above.")
    st.stop()

try:
    original_df = load_uploaded_file(file_name, file_bytes)
except Exception as exc:
    st.error(f"Could not read this file: {exc}")
    st.stop()

issues = analyze_dataframe(original_df)
summary = summarize_issues(issues)
issues["summary"] = summary

if summary["count"] == 0:
    st.success(summary["headline"])
else:
    st.warning(f"{summary['headline']}: {summary['details']}")

metric_columns = st.columns(4)
metric_columns[0].metric("Rows", f"{original_df.shape[0]:,}")
metric_columns[1].metric("Columns", f"{original_df.shape[1]:,}")
metric_columns[2].metric("Duplicate rows", f"{issues['duplicate_rows']:,}")
metric_columns[3].metric("Empty rows", f"{issues['empty_rows']:,}")

preview_tab, issues_tab, cleaning_tab = st.tabs(["Preview", "Issues", "Clean & Download"])

with preview_tab:
    st.subheader("First rows")
    st.dataframe(original_df.head(20), use_container_width=True)

with issues_tab:
    left, right = st.columns(2)

    with left:
        st.subheader("Detected issues")
        st.write(f"Empty rows: **{issues['empty_rows']:,}**")
        st.write(f"Duplicate rows: **{issues['duplicate_rows']:,}**")
        st.write("Empty columns:")
        st.write(issues["empty_columns"] or "None detected")
        st.write("Suspicious column names:")
        st.write(issues["suspicious_column_names"] or "None detected")
        st.write("Constant columns:")
        st.write(issues["constant_columns"] or "None detected")

    with right:
        st.subheader("Missing values by column")
        if issues["missing_values"]:
            missing_df = (
                pd.DataFrame(
                    [
                        {
                            "Column": column,
                            "Missing values": count,
                            "Missing %": issues["missing_percentages"][column],
                        }
                        for column, count in issues["missing_values"].items()
                    ],
                )
                .sort_values("Missing values", ascending=False)
                .reset_index(drop=True)
            )
            st.dataframe(missing_df, use_container_width=True, hide_index=True)
        else:
            st.success("No missing values detected.")

with cleaning_tab:
    st.subheader("Cleaning options")
    option_columns = st.columns(2)
    with option_columns[0]:
        strip_column_names = st.checkbox("Strip whitespace from column names", value=True)
        remove_empty_rows = st.checkbox("Remove fully empty rows", value=True)
    with option_columns[1]:
        remove_empty_columns = st.checkbox("Remove fully empty columns", value=True)
        remove_duplicate_rows = st.checkbox("Remove duplicate rows", value=True)

    cleaned_df, applied_steps = clean_dataframe(
        original_df,
        CleaningOptions(
            strip_column_names=strip_column_names,
            remove_empty_rows=remove_empty_rows,
            remove_empty_columns=remove_empty_columns,
            remove_duplicate_rows=remove_duplicate_rows,
        ),
    )
    report_html = generate_html_report(original_df, cleaned_df, issues, applied_steps)

    st.divider()
    before = f"{original_df.shape[0]:,} rows x {original_df.shape[1]:,} columns"
    after = f"{cleaned_df.shape[0]:,} rows x {cleaned_df.shape[1]:,} columns"
    st.write(f"Shape before cleaning: **{before}**")
    st.write(f"Shape after cleaning: **{after}**")
    st.write("Applied steps:")
    st.write(applied_steps)

    st.subheader("Cleaned preview")
    st.dataframe(cleaned_df.head(20), use_container_width=True)

    download_columns = st.columns(3)
    download_columns[0].download_button(
        "Download cleaned CSV",
        data=csv_bytes(cleaned_df),
        file_name="cleaned_data.csv",
        mime="text/csv",
        use_container_width=True,
    )
    download_columns[1].download_button(
        "Download cleaned XLSX",
        data=xlsx_bytes(cleaned_df),
        file_name="cleaned_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )
    download_columns[2].download_button(
        "Download HTML report",
        data=report_html,
        file_name="data_quality_report.html",
        mime="text/html",
        use_container_width=True,
    )

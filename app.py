import pandas as pd
import streamlit as st

from messy_data_cleaner import CleaningOptions, analyze_dataframe, clean_dataframe
from messy_data_cleaner.report import generate_html_report


st.set_page_config(page_title="Messy Data Cleaner", layout="wide")


@st.cache_data(show_spinner=False)
def load_uploaded_file(file_name: str, file_bytes: bytes) -> pd.DataFrame:
    from io import BytesIO

    buffer = BytesIO(file_bytes)
    if file_name.lower().endswith(".csv"):
        return pd.read_csv(buffer)
    if file_name.lower().endswith((".xlsx", ".xls")):
        return pd.read_excel(buffer)
    raise ValueError("Unsupported file type. Please upload a CSV or Excel file.")


def csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


st.title("Messy Data Cleaner")
st.caption("Upload a CSV or Excel file, review common quality issues, and download a cleaned file plus a simple HTML report.")

uploaded_file = st.file_uploader("Upload CSV or XLSX", type=["csv", "xlsx", "xls"])

if uploaded_file is None:
    st.info("Try the sample file in `examples/messy_sample.csv` or upload your own dataset.")
    st.stop()

try:
    original_df = load_uploaded_file(uploaded_file.name, uploaded_file.getvalue())
except Exception as exc:
    st.error(f"Could not read this file: {exc}")
    st.stop()

issues = analyze_dataframe(original_df)

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
                    issues["missing_values"].items(),
                    columns=["Column", "Missing values"],
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

    download_columns = st.columns(2)
    download_columns[0].download_button(
        "Download cleaned CSV",
        data=csv_bytes(cleaned_df),
        file_name="cleaned_data.csv",
        mime="text/csv",
        use_container_width=True,
    )
    download_columns[1].download_button(
        "Download HTML report",
        data=report_html,
        file_name="data_quality_report.html",
        mime="text/html",
        use_container_width=True,
    )

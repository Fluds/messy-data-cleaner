# Messy Data Cleaner

A minimal Streamlit app for uploading messy CSV or Excel files, spotting common data quality issues, and downloading a cleaned CSV plus a simple HTML report.

## Features

- Upload `.csv`, `.xlsx`, or `.xls` files
- Preview the first rows of the dataset
- Detect empty rows, empty columns, duplicate rows, missing values, suspicious column names, and constant columns
- Apply simple cleaning steps:
  - strip whitespace from column names
  - remove fully empty rows
  - remove fully empty columns
  - remove duplicate rows
- Download a cleaned CSV
- Download an HTML data quality report

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
streamlit run app.py
```

Open the local Streamlit URL, upload a CSV or Excel file, choose the cleaning options, then download the cleaned CSV and report.

A small sample file is available at:

```text
examples/messy_sample.csv
```

## Tests

```bash
pytest
```

## Screenshots

Placeholder:

![Messy Data Cleaner screenshot](docs/screenshot-placeholder.png)

## Limitations

- The app is designed for small to medium files that fit comfortably in memory.
- It does not infer data types, validate business rules, or fix malformed source files.
- Excel uploads read the first sheet only.
- Cleaning is intentionally conservative and limited to common structural issues.

# Messy Data Cleaner

Messy Data Cleaner is a small Streamlit app for quickly checking and cleaning CSV or Excel files before analysis.

It is built for analysts, students, researchers, and small teams who get spreadsheet-style data from forms, exports, surveys, lab notes, or shared team files and want a fast sanity check before working with it.

## What Problem It Solves

Real-world data often has small structural problems that slow down analysis:

- blank rows from copy/paste exports
- empty columns
- duplicate records
- missing values
- column names with hidden leading or trailing spaces
- columns that contain only one repeated value

Messy Data Cleaner detects those issues, applies conservative cleanup steps only when selected, and creates a simple report you can share or archive.

## What It Does In 30 Seconds

1. Upload a `.csv`, `.xlsx`, or `.xls` file.
2. Preview the first rows.
3. Review a plain-English summary of detected issues.
4. Choose simple cleaning options.
5. Download:
   - cleaned CSV
   - cleaned XLSX
   - HTML data quality report

You can also try the included sample dataset from inside the app.

## Run Locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

## Sample Data

A small messy sample file is included at:

```text
examples/messy_sample.csv
```

The app also includes buttons to use or download this sample file.

## Tests

```bash
pytest
```

## Deploy On Streamlit Community Cloud

1. Push this repository to GitHub.
2. Go to Streamlit Community Cloud.
3. Create a new app from the repository.
4. Set the main file path to:

```text
app.py
```

5. Deploy.

No secrets, API keys, database, or external services are required.

## Screenshots

Placeholder:

![Messy Data Cleaner screenshot](docs/screenshot-placeholder.png)

## Current Limitations

- Best for small to medium files that fit comfortably in memory.
- Excel uploads read the first sheet only.
- The app does not infer data types or validate domain-specific business rules.
- It does not repair malformed files.
- Cleaning is intentionally conservative and limited to common structural issues.
- Files are processed during the Streamlit session; there is no database or account system.

## Paid Customization

This demo can be adapted for team-specific workflows, reports, validation rules, or internal data templates.

Contact: add your preferred contact link or email here.

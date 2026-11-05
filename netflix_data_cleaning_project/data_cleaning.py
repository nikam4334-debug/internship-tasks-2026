"""
Task 1: Data Cleaning and Preprocessing
Run: python data_cleaning.py
Input: data/netflix_raw_sample.csv
Output: output/netflix_cleaned.csv and output/cleaning_summary.txt
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "data" / "netflix_raw_sample.csv"
OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(INPUT)
initial_rows = len(df)
initial_missing = int(df.isna().sum().sum())
initial_duplicates = int(df.duplicated().sum())

# 1. Clean column names.
df.columns = (df.columns.str.strip().str.lower().str.replace(" ", "_"))

# 2. Trim whitespace and standardize text fields.
text_cols = df.select_dtypes(include="object").columns
for col in text_cols:
    df[col] = df[col].map(lambda x: x.strip() if isinstance(x, str) else x)
    df[col] = df[col].replace("", pd.NA)

# 3. Standardize selected categorical values.
df["type"] = df["type"].str.strip().str.title()
df["type"] = df["type"].replace({"Tv Show": "TV Show"})
country_map = {
    "Usa": "United States", "U.S.A.": "United States", "U.S.": "United States",
    "Us": "United States", "Uk": "United Kingdom", "South Korea": "South Korea",
    "India": "India", "Canada": "Canada", "Australia": "Australia"
}
df["country"] = df["country"].str.title().replace(country_map)
df["duration"] = df["duration"].str.replace(r"\s+", " ", regex=True)
df["duration"] = df["duration"].str.replace(r"(?i)seasons?$", "Seasons", regex=True)
df["duration"] = df["duration"].str.replace(r"(?i)min$", "min", regex=True)

# 4. Parse date_added to a consistent datetime representation.
# format="mixed" supports datasets containing multiple date formats (pandas 2+).
try:
    df["date_added"] = pd.to_datetime(df["date_added"], format="mixed", errors="coerce")
except (TypeError, ValueError):
    df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")

# 5. Correct data types.
df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce").astype("Int64")

# 6. Handle missing values without inventing facts.
# Unknown descriptive fields remain blank; missing categorical fields get "Unknown".
for col in ["director", "cast", "country", "rating", "duration"]:
    df[col] = df[col].fillna("Unknown")

# 7. Remove exact duplicate records.
before_dedup = len(df)
df = df.drop_duplicates()
removed_duplicates = before_dedup - len(df)

# 8. Save cleaned data (dates use ISO YYYY-MM-DD format).
df["date_added"] = df["date_added"].dt.strftime("%Y-%m-%d")
df.to_csv(OUTPUT_DIR / "netflix_cleaned.csv", index=False)

final_missing = int(df.isna().sum().sum())
summary = f"""DATA CLEANING SUMMARY
Dataset: Netflix Movies and TV Shows (small practice sample)
Rows before cleaning: {initial_rows}
Rows after cleaning: {len(df)}
Exact duplicate rows detected initially: {initial_duplicates}
Duplicate rows removed: {removed_duplicates}
Missing cells before cleaning: {initial_missing}
Missing cells after cleaning: {final_missing}

CHANGES MADE
- Standardized column names to lowercase with underscores.
- Trimmed leading/trailing spaces in text fields.
- Standardized content type and selected country names.
- Standardized duration spacing and season wording.
- Converted date_added to YYYY-MM-DD; invalid or blank dates remain missing.
- Converted release_year to nullable integer.
- Replaced missing director, cast, country, rating and duration with "Unknown".
- Removed exact duplicate rows.
- Preserved records and avoided inventing missing information.

NOTE
This repository includes a small synthetic practice sample to demonstrate the workflow.
For a real-world internship submission, download the official Kaggle Netflix dataset,
place it at data/netflix_raw_sample.csv (or update INPUT in this script), and rerun.
"""
(OUTPUT_DIR / "cleaning_summary.txt").write_text(summary, encoding="utf-8")
print(summary)

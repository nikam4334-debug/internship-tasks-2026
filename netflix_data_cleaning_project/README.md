# Task 1 — Data Cleaning and Preprocessing

## Dataset
Netflix Movies and TV Shows dataset structure. This repository currently includes a **small synthetic practice sample** with deliberately introduced data-quality issues so the cleaning workflow can be demonstrated and tested.

For the full public dataset, use the Netflix Movies and TV Shows dataset on Kaggle:
https://www.kaggle.com/datasets/shivamb/netflix-shows

## Tools
- Python 3
- Pandas

## Project files
```text
netflix_data_cleaning_project/
├── data/
│   └── netflix_raw_sample.csv
├── output/
│   ├── netflix_cleaned.csv
│   └── cleaning_summary.txt
├── data_cleaning.py
├── requirements.txt
└── README.md
```

## Run on macOS
1. Open Terminal and move into this folder:
   `cd path/to/netflix_data_cleaning_project`
2. Install dependencies:
   `python3 -m pip install -r requirements.txt`
3. Run:
   `python3 data_cleaning.py`

The cleaned CSV and summary are saved in the `output` folder.

## Cleaning steps
1. Inspect missing values and duplicate records.
2. Standardize column names and trim text whitespace.
3. Standardize content type and selected country names.
4. Normalize duration text.
5. Parse `date_added` and convert `release_year` to a nullable integer.
6. Fill selected descriptive/category nulls with `Unknown`, without fabricating values.
7. Remove exact duplicate rows.
8. Export the cleaned dataset and a summary report.

## Important before submission
The included CSV is a **synthetic practice sample, not the original Kaggle dataset**. To submit work based on the real dataset, download `netflix_titles.csv` from the Kaggle link above, put it in `data/`, update the `INPUT` path at the top of `data_cleaning.py`, and rerun the script. Keep the raw and cleaned files in the repository if your internship instructions require them.

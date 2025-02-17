# Rearc Data Quest - Cloud Data Pipeline

## Overview

This repository contains the implementation of the **Rearc Data Quest**, a multi-step data engineering challenge that demonstrates skills in **AWS, Terraform, Python, and Data Analytics**. The project consists of four parts:

1. **AWS S3 & Sourcing Datasets** - Fetching data from the **Bureau of Labor Statistics (BLS)** and storing it in S3.
2. **APIs & Data Ingestion** - Extracting data from **DataUSA API** and storing it in S3.
3. **Data Analysis & Reporting** - Processing and analyzing data using **Pandas & Jupyter Notebooks**.
4. **Infrastructure as Code (IAC) & Automation** - Automating the pipeline with **Terraform & AWS Lambda** (In progress).

---

## Part 1: AWS S3 & Sourcing Datasets

### Goal

- Download **BLS time-series data** from `https://download.bls.gov/pub/time.series/pr/`
- Upload new files to **AWS S3 (****`arc-cloud-dq`****)**
- Keep S3 in sync (handle new, deleted, and modified files)

### Implementation

- **Script:** [`arc_bls_data_file_sync.py`](https://github.com/prasad4learning/cloud_dq/blob/main/arc_bls_data_file_sync.py)
- **Steps:**
  1. Extract filenames from the BLS website.
  2. Download new files to `bls_data/`.
  3. Upload the files to **AWS S3**.
  4. Keep the S3 bucket in sync by deleting outdated files.
  5. Log errors and ensure retries for failed downloads/uploads.

### Running the Script

```bash
python arc_bls_data_file_sync.py
```

---

## Part 2: APIs & Data Ingestion

### Goal

- Fetch **US population data** from the **DataUSA API** (`https://datausa.io/api/data?drilldowns=Nation&measures=Population`).
- Store the JSON response in **AWS S3**.

### Implementation

- **Script:** `arc_bls_data_file_sync.py` (combined with Part 1)
- **Steps:**
  1. Call the DataUSA API and fetch population data.
  2. Save the response as `datausa_population.json`.
  3. Upload the JSON file to **S3** (without duplicating existing files).

### Running the Script

```bash
python arc_bls_data_file_sync.py
```

---

## Part 3: Data Analysis & Reporting

### Goal

- Analyze the **BLS time-series data** (`pr.data.0.Current` from Part 1) and **US population data** (`datausa_population.json` from Part 2).
- Generate reports on trends and insights.

### Implementation

- **Notebooks:**
  - [`cloud_bls_data_analysis.ipynb`](https://github.com/prasad4learning/cloud_dq/blob/main/cloud_bls_data_analysis.ipynb)
  - [`arc_bls_data_analysis.ipynb`](https://github.com/prasad4learning/cloud_dq/blob/main/arc_bls_data_analysis.ipynb)

### Steps

1. **Load the data**

   - Read `pr.data.0.Current` as a DataFrame (CSV format).
   - Read `datausa_population.json` as a DataFrame (JSON format).

2. **Clean the Data**

   - Remove extra whitespaces.
   - Standardize column names.
   - Filter relevant years (2013-2018 for population data).

3. **Analysis & Reporting**

   - **US Population Statistics:** Compute **mean & standard deviation** of US population (2013-2018).
   - **Best Year per Series ID:** Find the **year with the highest total value** for each `series_id`.
   - **Series & Population Report:** Extract **c**values for `Q01` and match them with population data.

### Running the Analysis

Open the notebooks in Jupyter:

```bash
jupyter lab
```

Run the cells in **`cloud_bls_data_analysis.ipynb`** and **`arc_bls_data_analysis.ipynb`** to generate the reports.

---

## Next Steps

- **Part 4 (In Progress):** Automate the pipeline using **Terraform & AWS Lambda**.
- Implement **S3 event notifications** to trigger Lambda processing for new data.

---

## Author

**Prasad RK** | [GitHub](https://github.com/prasad4learning)

---

## References

- Rearc Data Quest Official Challenge
- [Bureau of Labor Statistics (BLS)](https://www.bls.gov/)
- [DataUSA API](https://datausa.io/about/api/)



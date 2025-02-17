# Cloud Data Quest - Cloud Data Pipeline

## Overview

This repository contains the implementation of the **Cloud Data Quest**, a multi-step data engineering challenge that demonstrates skills in **AWS, Terraform, Python, Jupyter Notebooks, and Data Analytics**. The project consists of four parts:

1. **AWS S3 & Sourcing Datasets** - Fetching data from the **Bureau of Labor Statistics (BLS)** and storing it in S3.
2. **APIs & Data Ingestion** - Extracting data from **DataUSA API** and storing it in S3.
3. **Data Analysis & Reporting** - Processing and analyzing data using **Pandas & Jupyter Notebooks**.
4. **Infrastructure as Code (IAC) & Automation** - Automating the pipeline with **Terraform, AWS Lambda, S3 Events, and SQS**.

---

## Part 1: AWS S3 & Sourcing Datasets

### Goal

- Download **BLS time-series data** from `https://download.bls.gov/pub/time.series/pr/`
- Upload new files to **AWS S3 (`arc-cloud-dq`)**
- Keep S3 in sync (handle new, deleted, and modified files)

### Implementation

- **Script:** [`arc_bls_data_file_sync.py`](https://github.com/prasad4learning/cloud_dq/blob/main/arc_bls_data_file_sync.py)
- **Steps:**
  1. Extract filenames from the BLS website.
  2. Download new files to `bls_data/`.
  3. Upload the files to **AWS S3**.
  4. Keep the S3 bucket in sync by deleting outdated files.
  5. Log errors and ensure retries for failed downloads/uploads.

### Challenges Faced

- **Parsing HTML for file extraction:** Required using BeautifulSoup to extract filenames correctly.
- **Handling API access issues:** Implemented proper `User-Agent` headers to avoid being blocked.
- **Ensuring idempotency:** The script avoids redundant uploads by checking for existing files in S3.

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

### Challenges Faced

- **Handling API rate limits:** Implemented retries with exponential backoff using `tenacity`.
- **Ensuring S3 consistency:** Preventing redundant uploads using S3 object checks.

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

### Significance of the Notebooks

#### `arc_bls_data_analysis.ipynb`
- Focuses on analyzing **BLS time-series data** to find trends in employment-related data.
- Includes steps for **data cleaning, transformation, and aggregations**.
- Identifies **best years per series_id** by summing quarterly values.

#### `cloud_bls_data_analysis.ipynb`
- Integrates **US population data** with **BLS time-series data**.
- Computes **mean & standard deviation of US population (2013-2018)**.
- Matches `series_id=PRS30006032` (if available) with population data, but **data was not found for this series_id**.

### Challenges Faced

- **Missing Data:** Some expected series_id values were not found.
- **Data Cleaning:** Required trimming spaces and handling missing values.
- **Performance:** Optimized large datasets using Pandas efficient operations.

### Running the Analysis

Open the notebooks in Jupyter:

```bash
jupyter lab
```

Run the cells in **`cloud_bls_data_analysis.ipynb`** and **`arc_bls_data_analysis.ipynb`** to generate the reports.

---

## Part 4: Infrastructure as Code & Automation

### Goal

- Automate the data pipeline using **Terraform & AWS Lambda**.
- Set up **S3 Event Notifications & SQS** to trigger Lambda processing.

### Implementation

- **Terraform Modules Used:**
  - **IAM Module:** Defines roles, policies, and permissions for Lambda execution.
  - **S3 Module:** Creates and manages the S3 bucket for storing data.
  - **Lambda Module:** Deploys a processing Lambda function.
  - **SQS Module:** Sets up an SQS queue for event-driven processing.

- **Lambda Functions Implemented:**
  - **Processing Lambda:** Handles S3 events and processes incoming data.
  - **Scheduled Lambda:** Runs Part 1 & Part 2 as a daily job.

- **IAM Roles & Policies:**
  - Created a **Lambda Execution Role** with `s3:GetObject`, `s3:PutObject`, `sqs:SendMessage`, and `logs:CreateLogStream` permissions.
  - Attached the necessary **IAM policies** to allow Lambda execution.

### Challenges Faced

- **IAM Permissions:** Required fine-tuning few policies to allow Lambda & S3 interactions.
- **Terraform Configuration Issues:** Encountered region mismatches (`eu-east-1` instead of `us-north-1`).
- **S3 Bucket Ownership Conflicts:** Fixed by verifying the bucket before attempting creation.

### Running Terraform Deployment

```bash

terraform init
terraform plan
terraform apply
```

---

## Key Takeaways

### What I Explored & Learned

- **Data Ingestion:** Handling public datasets via web scraping & API calls.
- **Cloud Storage:** Automating data synchronization with AWS S3.
- **Data Analytics:** Cleaning & processing large datasets using Pandas.
- **Infrastructure as Code:** Deploying cloud infrastructure with Terraform.
- **Event-Driven Architectures:** Using **S3 Event Notifications & SQS** to trigger processing.
- **AWS Lambda Functions:** Automating serverless data pipelines.
- **IAM & Security:** Managing policies & permissions for AWS resources.

---

## Author

**Prasad RK** | [GitHub](https://github.com/prasad4learning)

---

## References

- Cloud Data Quest Official Challenge
- [Bureau of Labor Statistics (BLS)](https://www.bls.gov/)
- [DataUSA API](https://datausa.io/about/api/)



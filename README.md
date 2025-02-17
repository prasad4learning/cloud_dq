#  Data Quest - Cloud Data Pipeline

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
## Parts 1 & 2: Data Ingestion and Storage

### Approach

I created a Python script (`arc_bls_data_file_sync.py`) to automate the process of fetching data from the BLS website and the Data USA API, and uploading it to an AWS S3 bucket (`arc-cloud-dq`).
*   Some files were removed due to their 404 faults.

### Libraries Used

*   `requests`: For making HTTP requests to fetch data from the BLS website and the Data USA API.
*   `boto3`: For interacting with AWS S3, including uploading files, listing bucket contents, and deleting files.
*   `beautifulsoup4`: For parsing HTML content from the BLS website to extract file names.
*   `re`: For using regular expressions to extract file names from the HTML content.
*   `logging`: For logging events and errors during the data synchronization process.
*   `argparse`: For defining command-line arguments to configure the script.
*   `tenacity`: For adding retry logic to handle potential network errors or temporary unavailability of the BLS website.

### Key Modules and Functions

*   `list_s3_files(s3_client, s3_bucket)`: Lists all files currently stored in the S3 bucket.
*   `download_file(file_url, local_path, headers)`: Downloads a file from the given URL with retry logic.
*   `upload_to_s3(s3_client, file_path, s3_bucket, file_name)`: Uploads a file to S3 with retry logic.
*   `fetch_data_from_api(api_url, headers=None)`: Fetches data from an API endpoint.
*   `save_json_to_s3(s3_client, data, s3_bucket, file_name)`: Saves JSON data to an S3 bucket.
*   `main()`: The main function that orchestrates the entire data synchronization process.

### Running the Script

1.  **Install Dependencies:**

    ```
    pip install requests beautifulsoup4 boto3 argparse tenacity
    ```

2.  **Configure AWS Credentials:**

    *   Ensure your AWS credentials are configured correctly.  Use `aws configure`.

3.  **Execute the Script:**

    ```
    python arc_bls_data_file_sync.py
    ```

## Part 3: Data Analysis and Report Generation

### Approach

I used a Jupyter Notebook (`rearc_data_quest_part3.ipynb`) with pandas to perform data analysis and generate reports based on the data stored in S3.

### Libraries Used

*   `pandas`: For data manipulation and analysis.
*   `boto3`: For reading data from S3.
*   `json`: For handling JSON data.
*   `io`: For working with in-memory data streams.

### Analysis Steps

1.  **Load Data:** Load the CSV file from Part 1 (`pr.data.0.Current`) and the JSON file from Part 2 (`datausa_population.json`) into Pandas DataFrames.
2.  **Population Data Analysis:**
    *   Filter the population DataFrame to include only the years 2013 to 2018 (inclusive).
    *   Calculate the mean and standard deviation of the "Population" column for the filtered data.
3.  **Time-Series Data Analysis:**
    *   For every `series_id`, find the best year (the year with the largest sum of "value" for all quarters in that year).
    *   Generate a report with each `series_id`, the best year for that series, and the summed value for that year.
4.  **Combined Data Analysis:**
    *   Generate a report that provides the value for `series_id = PRS30006032` and `period = Q01` and the population for that given year (if available in the population dataset).

### Challenges Faced

*   **Data Cleaning:** Public datasets often require data cleaning. I used `str.strip()` to remove leading/trailing whitespace and `astype()` to convert columns to the correct data types.
*   **PRS30006032 Data:** I was unable to find data for `series_id = PRS30006032` in the BLS dataset. As a result, the combined data analysis report may be incomplete.

## Part 4: Infrastructure as Code (Terraform)

I am currently working on Part 4 of the Rearc Data Quest, which involves automating the data pipeline using Infrastructure as Code (Terraform).

### Goal

*   To provision and manage the AWS resources required for the data pipeline using Terraform.
*   This includes:
    *   S3 bucket for storing the data.
    *   SQS queue for receiving S3 event notifications.
    *   Lambda functions for executing Parts 1, 2, and 3.
    *   CloudWatch Events rule for scheduling the data synchronization Lambda function.
    *   IAM roles and policies for granting the necessary permissions to the Lambda functions.

### Terraform Modules

The Terraform configuration is organized into modules for better maintainability and reusability.

*   **`main.tf`**: Contains S3, IAM Role, and the Lambda function and schedule
*   **`variables.tf`**: Defines the input variables for the Terraform configuration.
*   **`outputs.tf`**: Defines the output values that will be displayed after the Terraform configuration is applied.

### Challenges

*   Configuring the Terraform provider and authenticating with AWS.
*   Defining the resources and configuring the IAM roles, function, and triggers.
*   Automating and linking the functions
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

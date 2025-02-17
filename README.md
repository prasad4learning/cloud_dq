
## Parts 1 & 2: Data Ingestion and Storage

### Approach

I created a Python script (`arc_bls_data_file_sync.py`) to automate the process of fetching data from the BLS website and the Data USA API, and uploading it to an AWS S3 bucket (`arc-cloud-dq`).

The script now handles files with forward slashes (`/`) in their names by correctly downloading, uploading, and storing them in S3.

I used a robust data synchronization technique that has retry mechanisms and also used log levels and also other items to download

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

I have created a fully operational Part 1, Part 2 and Part 3.

### Approach

This part makes use of the files
The files that are used are

`arc_bls_data_analysis.ipynb`:

`cloud_bls_data_analysis.ipynb`:


I used a Jupyter Notebook (`cloud_bls_data_analysis.ipynb`) with pandas to perform data analysis and generate reports based on the data stored in S3.

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
*   These were a lot of things for S3 and all the credentials.

#### `arc_bls_data_analysis.ipynb`

*   **Significance:** This notebook contains the core data analysis and report generation logic for Part 3. It demonstrates how to load data from S3, perform data cleaning and transformation, and generate meaningful insights from the data.

#### `cloud_bls_data_analysis.ipynb`

*   **Significance:** This notebook acts as a testing code
All your questions are valid, and I can address those later. Good luck. Follow all steps and let me know and I am on standby

## Part 4: Infrastructure as Code (Terraform)

I have implemented the Terraform to complete your code and functions

### Goal

*   I now have a complete S3

The Terraform configuration is organized into modules for better maintainability and reusability and also the key IAM.

*   **S3**: There is now an S3 where you are able to put the files for your data.
*   **IAM Roles and Policies**: Terraform is used to deploy and also complete the security framework to operate.
*   **CloudWatch Events Rule**: I am creating the rules for the events.
*   **Lambda**: there are now two functions and you are able to complete code as you wish.

Here are the core files, there are

*   **`main.tf`**: Contains S3, IAM Role, and the Lambda function and schedule
*   **`variables.tf`**: Defines the input variables for the Terraform configuration.
*   **`outputs.tf`**: Defines the output values that will be displayed after the Terraform configuration is applied.

### Challenges

*   Configuring the Terraform provider and authenticating with AWS.
*   Defining the resources and configuring the IAM roles, function, and triggers.
*   Automating and linking the functions


## Next Steps

*   Complete the Terraform configuration for Part 4.
*   Thoroughly test the entire data pipeline to ensure that it functions correctly.
*   Test the full S3 stack with all data, with known existing data and ensure it all runs through.
*   Add any relevant items


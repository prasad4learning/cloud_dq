"""
Rearc Data Quest - Part 1 & 2: AWS S3 & Data Sync

Author: Prasad RK (prasad4learning@gmail.com)
Purpose:
- Fetch BLS dataset from https://download.bls.gov/pub/time.series/pr/
- Upload new files to AWS S3 (`arc-cloud-dq`)
- Fetch data from DataUSA API and store in S3
"""

import os
import requests
import boto3
from botocore.exceptions import NoCredentialsError, BotoCoreError
from bs4 import BeautifulSoup
import logging
import re
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from requests.exceptions import RequestException
import json

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# --- AWS & Data Config ---
S3_BUCKET = "arc-cloud-dq"  # Ensure this bucket exists
S3_REGION = "us-east-1"
BLS_BASE_URL = "https://download.bls.gov/pub/time.series/pr/"
DATAUSA_API_URL = "https://datausa.io/api/data?drilldowns=Nation&measures=Population"
HEADERS = {"User-Agent": "prasad4learning@gmail.com"}  # Set your contact email

# Create S3 Client
try:
    s3 = boto3.client("s3", region_name=S3_REGION)
except BotoCoreError as e:
    logger.error(f"❌ AWS S3 Initialization Failed: {e}")
    exit(1)

# --- Function Definitions ---

def list_s3_files():
    """List files stored in the S3 bucket."""
    try:
        response = s3.list_objects_v2(Bucket=S3_BUCKET)
        return {obj["Key"] for obj in response.get("Contents", [])} if "Contents" in response else set()
    except NoCredentialsError:
        logger.error("❌ AWS credentials not found.")
        return set()
    except BotoCoreError as e:
        logger.error(f"❌ Error listing S3 files: {e}")
        return set()

def extract_filenames(html_content):
    """Extract valid file names from the BLS HTML directory listing."""
    soup = BeautifulSoup(html_content, "html.parser")
    pre_tag = soup.find("pre")

    if not pre_tag:
        logger.error("❌ Failed to find <pre> tag on BLS website. Parsing failed.")
        return []

    # Extract only valid filenames (skip invalid timestamped filenames)
    file_names = re.findall(r'pr\.[a-zA-Z0-9._-]+(?=\s|<)', pre_tag.get_text())

    logger.info(f"🔍 Extracted {len(file_names)} filenames from BLS: {file_names}")
    return file_names

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=5), retry=retry_if_exception_type(RequestException))
def download_file(file_url, local_path):
    """Download a file with retry logic."""
    try:
        logger.info(f"⬇️ Downloading {file_url}...")
        response = requests.get(file_url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        with open(local_path, "wb") as f:
            f.write(response.content)
        logger.info(f"✅ Successfully downloaded {os.path.basename(local_path)}")
    except RequestException as e:
        logger.error(f"❌ Download failed for {file_url}: {e}")
        raise

def download_bls_files():
    """Download all available BLS dataset files."""
    logger.info("🔍 Fetching file list from BLS website...")
    response = requests.get(BLS_BASE_URL, headers=HEADERS)
    
    if response.status_code != 200:
        logger.error(f"❌ Failed to fetch BLS file list. HTTP Status: {response.status_code}")
        return
    
    files = extract_filenames(response.text)
    os.makedirs("bls_data", exist_ok=True)

    for file in files:
        file_url = BLS_BASE_URL + file

        # **Skip if URL returns 404**
        if requests.head(file_url, headers=HEADERS).status_code == 404:
            logger.warning(f"⚠️ Skipping {file} (URL not found)")
            continue

        local_path = os.path.join("bls_data", file)
        download_file(file_url, local_path)

def upload_to_s3():
    """Upload new files from local directory to S3."""
    local_files = set(os.listdir("bls_data"))
    s3_files = list_s3_files()

    logger.info(f"📤 Checking for new files to upload: {local_files - s3_files}")
    for file in local_files:
        if file not in s3_files:
            file_path = os.path.join("bls_data", file)
            try:
                logger.info(f"📤 Uploading {file} to S3...")
                s3.upload_file(file_path, S3_BUCKET, file)
                logger.info(f"✅ Uploaded {file} to S3!")
            except BotoCoreError as e:
                logger.error(f"❌ Failed to upload {file} to S3: {e}")

def delete_removed_files():
    """Delete files from S3 that no longer exist in BLS dataset."""
    local_files = set(os.listdir("bls_data"))
    s3_files = list_s3_files()

    for file in s3_files - local_files:
        try:
            logger.info(f"🗑️ Deleting {file} from S3...")
            s3.delete_object(Bucket=S3_BUCKET, Key=file)
            logger.info(f"✅ Deleted {file} from S3!")
        except BotoCoreError as e:
            logger.error(f"❌ Failed to delete {file} from S3: {e}")

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=5), retry=retry_if_exception_type(RequestException))
def fetch_datausa_population():
    """Fetches population data from the DataUSA API."""
    try:
        logger.info(f"🌎 Fetching population data from {DATAUSA_API_URL}...")
        response = requests.get(DATAUSA_API_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        logger.error(f"❌ Failed to fetch API data: {e}")
        raise

def save_json_to_s3(data, file_name="datausa_population.json"):
    """Save JSON data to S3."""
    try:
        json_string = json.dumps(data, indent=2)
        s3.put_object(Bucket=S3_BUCKET, Key=file_name, Body=json_string)
        logger.info(f"✅ Saved JSON data to s3://{S3_BUCKET}/{file_name}")
    except BotoCoreError as e:
        logger.error(f"❌ Failed to save JSON to S3: {e}")

def main():
    """Main function to execute the data synchronization process."""
    logger.info("🚀 Starting BLS & DataUSA Sync Process...")

    # Download BLS data and sync with S3
    download_bls_files()
    upload_to_s3()
    delete_removed_files()

    # Fetch and save DataUSA API data
    api_data = fetch_datausa_population()
    save_json_to_s3(api_data)

    logger.info("✅ Sync completed successfully!")

if __name__ == "__main__":
    main()


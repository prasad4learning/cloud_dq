import json
import boto3
import logging

# Configure Logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS Clients
s3_client = boto3.client("s3")

def process_sqs(event, context):
    """
    Lambda function triggered by SQS to process new data and log insights.
    
    Args:
        event (dict): SQS event containing S3 notification messages.
        context (object): Lambda execution context.
    """
    logger.info("📥 Received SQS Event: %s", json.dumps(event, indent=2))

    for record in event.get("Records", []):
        try:
            # Extract S3 bucket and object key from the message
            message_body = json.loads(record["body"])
            s3_info = message_body["Records"][0]["s3"]
            bucket_name = s3_info["bucket"]["name"]
            object_key = s3_info["object"]["key"]

            logger.info(f"📂 Processing new S3 object: s3://{bucket_name}/{object_key}")

            # Read JSON data from S3
            response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
            json_data = json.loads(response["Body"].read().decode("utf-8"))

            # Extract relevant fields
            logger.info(f"📊 Extracted Data from {object_key}: {json.dumps(json_data, indent=2)}")

        except Exception as e:
            logger.error(f"❌ Failed to process message: {e}", exc_info=True)

    return {"status": "success"}


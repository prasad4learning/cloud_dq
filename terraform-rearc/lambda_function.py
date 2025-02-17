import json
import boto3

def lambda_handler(event, context):
    print("Lambda function triggered")
    print("Event:", json.dumps(event, indent=2))
    
    return {
        "statusCode": 200,
        "body": json.dumps("Lambda executed successfully!")
    }


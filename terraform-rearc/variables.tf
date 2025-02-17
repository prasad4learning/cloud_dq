variable "aws_region" {
  description = "AWS region"
  default     = "us-east-1"
}

variable "s3_bucket" {
  description = "S3 bucket for storing datasets"
  default     = "arc-cloud-dq"
}

variable "lambda_execution_role" {
  description = "IAM Role for Lambda execution"
  default     = "rearc_lambda_execution_role"
}

variable "sqs_queue_name" {
  description = "SQS queue for S3 event notifications"
  default     = "rearc_data_queue"
}

variable "bls_lambda_function_name" {
  description = "Lambda function to fetch BLS and DataUSA data"
  default     = "rearc_bls_data_lambda"
}

variable "processing_lambda_function_name" {
  description = "Lambda function to process SQS messages"
  default     = "rearc_data_processing_lambda"
}


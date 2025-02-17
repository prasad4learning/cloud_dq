resource "aws_lambda_function" "processing_lambda" {
  function_name = "processing_lambda"
  
  role          = aws_iam_role.lambda_execution_role.arn  # IAM Role reference

  # Lambda function execution environment
  environment {
    variables = {
      SQS_QUEUE_URL = aws_sqs_queue.existing_queue.url
    }
  }

  # Lambda function details like handler, runtime, etc.
  handler = "lambda_function.lambda_handler"
  runtime = "python3.8"

  filename = "lambda_package.zip"  # Ensure you upload your Lambda function package
}



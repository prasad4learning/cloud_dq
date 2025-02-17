resource "aws_lambda_function" "processing_lambda" {
  function_name    = "rearc_data_processing_lambda"
  role            = aws_iam_role.lambda_execution_role.arn
  runtime        = "python3.8"
  handler        = "lambda_function.lambda_handler"
  filename       = "lambda_package.zip"

  source_code_hash = filebase64sha256("lambda_package.zip")

  environment {
    variables = {
      S3_BUCKET = data.aws_s3_bucket.existing_bucket.id
      SQS_QUEUE_URL = aws_sqs_queue.data_queue.id
    }
  }

  depends_on = [aws_iam_role_policy_attachment.lambda_policy_attachment]
}


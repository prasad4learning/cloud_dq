output "s3_bucket_name" {
  value = data.aws_s3_bucket.existing_bucket.id
}

output "lambda_function_name" {
  value = aws_lambda_function.processing_lambda.function_name
}

output "sqs_queue_url" {
  value = aws_sqs_queue.data_queue.url
}


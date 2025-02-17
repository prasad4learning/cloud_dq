# SQS Queue Creation
resource "aws_sqs_queue" "existing_queue" {
  name = "rearc_data_queue"  # The name of your SQS queue
}

# SQS Queue Policy to allow S3 to send messages to the queue
resource "aws_sqs_queue_policy" "s3_to_sqs_policy" {
  queue_url = aws_sqs_queue.existing_queue.url

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Action    = "SQS:SendMessage"
        Principal = "*"
        Resource  = aws_sqs_queue.existing_queue.arn
        Condition = {
          ArnEquals = {
            "aws:SourceArn" = data.aws_s3_bucket.existing_bucket.arn
          }
        }
      }
    ]
  })
}


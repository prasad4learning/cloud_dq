# Reference the existing S3 bucket
data "aws_s3_bucket" "existing_bucket" {
  bucket = "arc-cloud-dq"  # Your existing bucket name
}

# S3 Bucket notification configuration to trigger on new objects (suffix .json)
resource "aws_s3_bucket_notification" "s3_event" {
  bucket = data.aws_s3_bucket.existing_bucket.id

  queue {
    id           = "s3-to-sqs-notification"
    queue_arn    = aws_sqs_queue.existing_queue.arn
    events       = ["s3:ObjectCreated:Put"]
    filter_suffix = ".json"
  }

  depends_on = [aws_sqs_queue_policy.s3_to_sqs_policy]
}

# S3 Bucket Policy
resource "aws_s3_bucket_policy" "existing_bucket_policy" {
  bucket = data.aws_s3_bucket.existing_bucket.id

  policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Action    = "s3:GetObject"
        Principal = "*"
        Resource  = "${data.aws_s3_bucket.existing_bucket.arn}/*"
      }
    ]
  })
}


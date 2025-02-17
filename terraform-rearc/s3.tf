data "aws_s3_bucket" "existing_bucket" {
  bucket = "arc-cloud-dq"
  provider = aws  # Ensures it uses the provider region
}

resource "aws_s3_bucket" "existing_bucket" {
  bucket = "arc-cloud-dq"
  force_destroy = true
}

resource "aws_s3_bucket_acl" "data_bucket_acl" {
  bucket = data.aws_s3_bucket.existing_bucket.id
  acl    = "private"
}

resource "aws_s3_bucket_notification" "s3_event" {
  bucket = data.aws_s3_bucket.existing_bucket.id

  queue {
    queue_arn = aws_sqs_queue.data_queue.arn
    events    = ["s3:ObjectCreated:*"]
  }
}


# S3 Bucket Policy - Renamed resource to avoid conflict
resource "aws_s3_bucket_policy" "existing_bucket_policy_s3bkt" {  # Renamed resource name
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


resource "aws_sqs_queue" "data_queue" {
  name                      = "rearc_data_queue"
  delay_seconds             = 0
  visibility_timeout_seconds = 60
  message_retention_seconds = 86400
}


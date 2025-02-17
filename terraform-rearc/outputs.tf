output "sqs_queue_url" {
  value = aws_sqs_queue.existing_queue.url  # Updated reference
}


resource "aws_iam_role" "lambda_execution_role" {
  name = "rearc_lambda_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_policy" "lambda_policy" {
  name        = "rearc_lambda_policy"
  description = "IAM policy for Rearc Lambda function"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:PutObject", "s3:ListBucket", "s3:DeleteObject"]
        Resource = [
          "arn:aws:s3:::arc-cloud-dq",
          "arn:aws:s3:::arc-cloud-dq/*"
        ]
      },
      {
        Effect   = "Allow"
        Action   = ["sqs:SendMessage", "sqs:ReceiveMessage", "sqs:DeleteMessage"]
        Resource = aws_sqs_queue.data_queue.arn
      },
      {
        Effect   = "Allow"
        Action   = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
        Resource = "arn:aws:logs:eu-north-1:183295436581:*"
      },
      {
        Effect   = "Allow"
        Action   = ["lambda:InvokeFunction", "lambda:CreateFunction", "lambda:GetFunction", "lambda:UpdateFunctionCode", "iam:PassRole"]
        Resource = "arn:aws:lambda:eu-north-1:183295436581:function:rearc_data_processing_lambda"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}


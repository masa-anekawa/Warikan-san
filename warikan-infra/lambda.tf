resource "aws_lambda_function" "csv_transformer" {
  depends_on = [
    aws_iam_role_policy_attachment.lambda_logs,
    aws_cloudwatch_log_group.lambda_log_group,
  ]

  function_name = "${var.app_name}-csv-transformer"
  role          = aws_iam_role.lambda_exec.arn
  package_type  = "Image"
  image_uri = "${aws_ecr_repository.lambda_container_repo.repository_url}:b1c3557ee4322e440677ace1855a9780"
  timeout       = 60  # 必要に応じてタイムアウトを調整

  environment {
    variables = {
      OUTPUT_BUCKET = aws_s3_bucket.output_bucket.bucket
    }
  }
}

resource "aws_iam_role" "lambda_exec" {
  name = "${var.app_name}_lambda_exec_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Principal = {
          Service = "lambda.amazonaws.com"
        },
        Effect = "Allow",
        Sid    = ""
      }
    ]
  })
}

import {
  to = aws_cloudwatch_log_group.lambda_log_group
  id = "/aws/lambda/warikan-san_csv_transformer"
}

resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/${var.app_name}_csv_transformer"
  retention_in_days = 14
}

data "aws_iam_policy_document" "lambda_logging" {
  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]

    resources = ["arn:aws:logs:*:*:*"]
  }
}

resource "aws_iam_policy" "lambda_logging" {
  name        = "lambda_logging"
  path        = "/"
  description = "IAM policy for logging from a lambda"
  policy      = data.aws_iam_policy_document.lambda_logging.json
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}
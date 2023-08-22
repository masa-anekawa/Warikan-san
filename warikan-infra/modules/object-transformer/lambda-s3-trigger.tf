resource "aws_s3_bucket_notification" "bucket_notification" {
  depends_on   = [null_resource.wait_for_lambda_trigger]
  bucket = aws_s3_bucket.input_bucket.bucket

  lambda_function {
    lambda_function_arn = aws_lambda_function.csv_formatter.arn
    events              = ["s3:ObjectCreated:*"]
  }
}

resource "null_resource" "wait_for_lambda_trigger" {
  depends_on   = [aws_lambda_permission.allow_bucket]
  provisioner "local-exec" {
    command = "sleep 10s"
  }
}

resource "aws_lambda_permission" "allow_bucket" {
  statement_id  = "AllowS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.csv_formatter.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.input_bucket.arn
}

resource "aws_iam_role_policy_attachment" "lambda_s3_access" {
  policy_arn = aws_iam_policy.lambda_s3_access.arn
  role       = aws_iam_role.lambda_exec.name
}

resource "aws_iam_policy" "lambda_s3_access" {
  name        = "${var.project_name}_LambdaS3Access"
  description = "Allows lambda to read and write from S3"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "s3:GetObject",
        ],
        Resource = [
          "${aws_s3_bucket.input_bucket.arn}/*",
        ],
        Effect = "Allow"
      },
      {
        Action = [
          "s3:PutObject"
        ],
        Resource = [
          "${aws_s3_bucket.output_bucket.arn}/*"
        ],
        Effect = "Allow"
      }
    ]
  })
}

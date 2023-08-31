output "output_bucket_name" {
  description = "The name of the S3 bucket where transformed objects are placed."
  value       = aws_s3_bucket.output_bucket.bucket
}

output "lambda_function_arn" {
  description = "The ARN of the Lambda function."
  value       = aws_lambda_function.csv_formatter.arn
}

output "iam_role_arn" {
  description = "The ARN of the IAM role used by the Lambda function."
  value       = aws_iam_role.lambda_exec.arn
}

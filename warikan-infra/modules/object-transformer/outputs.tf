output "output_bucket" {
  description = "The S3 bucket where transformed objects are placed."
  value       = aws_s3_bucket.output_bucket
}

output "lambda_function_arn" {
  description = "The ARN of the Lambda function."
  value       = aws_lambda_function.lambda_function.arn
}

output "iam_role_arn" {
  description = "The ARN of the IAM role used by the Lambda function."
  value       = aws_iam_role.lambda_exec.arn
}

output "iam_role_name" {
  description = "The name of the IAM role used by the Lambda function."
  value       = aws_iam_role.lambda_exec.name
}

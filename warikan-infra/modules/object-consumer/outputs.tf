output "lambda_function_arn" {
  description = "The ARN of the Lambda function."
  value       = aws_lambda_function.lambda_function.arn
}

output "iam_role_arn" {
  description = "The ARN of the IAM role used by the Lambda function."
  value       = aws_iam_role.lambda_exec.arn
}

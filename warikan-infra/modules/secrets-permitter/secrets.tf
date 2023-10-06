# Load the secrets JSON file as a data source
data "local_file" "secret_json" {
  filename = "${path.module}/secrets.json"
}

# Create the secrets in AWS Secrets Manager
resource "aws_secretsmanager_secret" "this" {
  name = "${var.project_name}-${var.name}-secrets"
}

resource "aws_secretsmanager_secret_version" "my_secret_version" {
  secret_id     = aws_secretsmanager_secret.this.id
  secret_string = data.local_file.secret_json.content
}

resource "aws_iam_role_policy_attachment" "lambda_secrets_manager_access" {
  role       = var.requester_role_name
  policy_arn = "arn:aws:iam::aws:policy/SecretsManagerReadWrite"
}


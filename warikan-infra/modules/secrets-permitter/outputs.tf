output "secret_name_env_map" {
  description = "The map of the environment variable that contains the name of the secrets."
  value       = {
    SECRETS_NAME = aws_secretsmanager_secret.this.name
  }
}

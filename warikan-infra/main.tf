provider "aws" {
  region = var.region
}

locals {
  secrets_name = "${var.app_name}-gspread-writer-secrets"
}

module "encoding_adjuster" {
  source       = "./modules/object-transformer"
  region       = var.region
  account_id   = var.account_id
  project_name = var.app_name
  name         = "encoding-adjuster"
  input_bucket = aws_s3_bucket.initial_bucket
  image_uri    = "${var.account_id}.dkr.ecr.${var.region}.amazonaws.com/warikan-san-encoding-adjuster:6cf6bbf655f43ce4e5092df4d692248f"
}

module "warikan_detector" {
  source       = "./modules/object-transformer"
  region       = var.region
  account_id   = var.account_id
  project_name = var.app_name
  name         = "warikan-detector"
  input_bucket = module.encoding_adjuster.output_bucket
  image_uri    = "${var.account_id}.dkr.ecr.${var.region}.amazonaws.com/warikan-san-warikan-detector:4eb20e9d3caf2874a4a12d5b78a467cb"
}

module "csv_formatter" {
  source       = "./modules/object-transformer"
  region       = var.region
  account_id   = var.account_id
  project_name = var.app_name
  name         = "csv-formatter"
  input_bucket = aws_s3_bucket.confirmed_bucket
  image_uri    = "${var.account_id}.dkr.ecr.${var.region}.amazonaws.com/warikan-san-csv-formatter:c6fe22b9545140fb17cec29e906f7473"
}

module "gspread_writer" {
  source       = "./modules/object-consumer"
  region       = var.region
  account_id   = var.account_id
  project_name = var.app_name
  name         = "gspread-writer"
  input_bucket = module.csv_formatter.output_bucket
  image_uri    = "${var.account_id}.dkr.ecr.${var.region}.amazonaws.com/warikan-san-gspread-writer:b293bcf26a04a1f3f8c6d9526d94a5c2"
  custom_environment_variables = {
    SECRETS_NAME = local.secrets_name
  }
}

module "gspread_secrets_permitter" {
  source              = "./modules/secrets-permitter"
  secrets_name        = local.secrets_name
  requester_role_name = module.gspread_writer.iam_role_name
}

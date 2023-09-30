provider "aws" {
  region = var.region
}

module "encoding_adjuster" {
  source       = "./modules/object-transformer"
  region       = var.region
  account_id   = var.account_id
  project_name = var.app_name
  name         = "encoding-adjuster"
  input_bucket = aws_s3_bucket.test_bucket
  image_uri    = "${var.account_id}.dkr.ecr.${var.region}.amazonaws.com/warikan-san-encoding-adjuster:6cf6bbf655f43ce4e5092df4d692248f"
}

module "warikan-detector" {
  source       = "./modules/object-transformer"
  region       = var.region
  account_id   = var.account_id
  project_name = var.app_name
  name         = "warikan-detector"
  input_bucket = aws_s3_bucket.test_bucket
  image_uri    = "${var.account_id}.dkr.ecr.${var.region}.amazonaws.com/warikan-san-warikan-detector:4eb20e9d3caf2874a4a12d5b78a467cb"
}

module "csv_formatter" {
  source       = "./modules/object-transformer"
  region       = var.region
  account_id   = var.account_id
  project_name = var.app_name
  name         = "csv-formatter"
  input_bucket = aws_s3_bucket.initial_bucket
  image_uri    = "${var.account_id}.dkr.ecr.${var.region}.amazonaws.com/warikan-san-csv-formatter:c6fe22b9545140fb17cec29e906f7473"
}

module "gspread-writer" {
  source       = "./modules/object-consumer"
  region       = var.region
  account_id   = var.account_id
  project_name = var.app_name
  name         = "gspread-writer"
  input_bucket = module.csv_formatter.output_bucket
  image_uri    = "${var.account_id}.dkr.ecr.${var.region}.amazonaws.com/warikan-san-gspread-writer:ad50b20f004137e739591f29741e6eeb"
}
provider "aws" {
  region = var.region
}


module "csv_formatter" {
  source       = "./modules/object-transformer"
  region       = var.region
  account_id   = var.account_id
  project_name = var.app_name
  name         = "csv-formatter"
  input_bucket = aws_s3_bucket.initial_bucket
  image_uri    = "${var.account_id}.dkr.ecr.${var.region}.amazonaws.com/warikan-san-csv-formatter:6040c7d72d28553000819fcf28f6dcca"
}

module "warikan-detector" {
  source       = "./modules/object-transformer"
  region       = var.region
  account_id   = var.account_id
  project_name = var.app_name
  name         = "warikan-detector"
  input_bucket = aws_s3_bucket.test_bucket
  image_uri    = "${var.account_id}.dkr.ecr.${var.region}.amazonaws.com/warikan-san-warikan-detector:81849ac2e22a579b4add46a6001cb31b"
}
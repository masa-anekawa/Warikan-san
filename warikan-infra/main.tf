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
  image_uri    = "${var.account_id}.dkr.ecr.${var.region}.amazonaws.com/warikan-san-csv-formatter:cfbfca3a6663af7d0d8363cafb6b7f2a"
}

module "warikan-detector" {
  source       = "./modules/object-transformer"
  region       = var.region
  account_id   = var.account_id
  project_name = var.app_name
  name         = "warikan-detector"
  input_bucket = aws_s3_bucket.test_bucket
  image_uri    = "${var.account_id}.dkr.ecr.${var.region}.amazonaws.com/warikan-san-warikan-detector:7f26ca752deb28e50058bbf0ee2f19fa"
}
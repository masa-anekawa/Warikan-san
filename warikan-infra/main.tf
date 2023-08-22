provider "aws" {
  region = "ap-northeast-1"
}

module "csv_formatter" {
  source           = "./modules/object-transformer"
  project_name     = var.app_name
  name             = "csv-formatter"
  image_uri        = "299550732592.dkr.ecr.ap-northeast-1.amazonaws.com/warikan-san-csv-formatter:cfbfca3a6663af7d0d8363cafb6b7f2a"
}
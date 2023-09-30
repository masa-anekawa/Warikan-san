# region variable
variable "region" {
  description = "The AWS region to deploy to."
  type        = string
}

# aws account id variable
variable "account_id" {
  description = "The AWS account ID to deploy to."
  type        = string
}

variable "project_name" {
  description = "The name of the application."
  type        = string
}

variable "name" {
  description = "The name of the object transformer."
  type        = string
}

# input_bucket map variable that has 'bucket' and 'arn' as key and striings as values

variable "input_bucket" {
  description = "The S3 bucket where initial objects are placed."
  type        = object({
    bucket = string
    arn    = string
  })
}

variable "image_uri" {
  description = "The URI of the container image used by the Lambda function."
  type        = string
}

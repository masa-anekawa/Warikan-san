variable "app_name" {
  description = "The name of the application to use as a prefix for resources."
  default     = "warikan-san"
}

variable "region" {
  description = "The AWS region to deploy to."
  type        = string
  default     = "ap-northeast-1"
}

variable "account_id" {
  description = "The AWS account ID to deploy to."
  type        = string
}

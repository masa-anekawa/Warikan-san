variable "project_name" {
  description = "The name of the application."
  type        = string
}

variable "name" {
  description = "The name of the object transformer."
  type        = string
}

variable "image_uri" {
  description = "The URI of the container image used by the Lambda function."
  type        = string
}

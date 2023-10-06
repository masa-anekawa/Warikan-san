variable "project_name" {
  description = "The name of the application."
  type        = string
}

variable "name" {
  description = "The name of the object transformer."
  type        = string
}

variable "requester_role_name" {
  description = "The name of the role that is allowed to request the secrets."
  type        = string
}

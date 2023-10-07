variable "secrets_name" {
  description = "The name of the secrets."
  type        = string
}

variable "requester_role_name" {
  description = "The name of the role that is allowed to request the secrets."
  type        = string
}

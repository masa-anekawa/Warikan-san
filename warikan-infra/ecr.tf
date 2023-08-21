resource "aws_ecr_repository" "lambda_container_repo" {
  name                 = "${var.app_name}-lambda-container"
  image_tag_mutability = "MUTABLE"
}

resource "aws_ecr_lifecycle_policy" "lambda_container_lifecycle" {
  repository = aws_ecr_repository.lambda_container_repo.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep last 10 images"
        selection = {
          tagStatus   = "any"
          countType   = "imageCountMoreThan"
          countNumber = 10
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}

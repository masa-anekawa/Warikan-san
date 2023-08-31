resource "aws_s3_bucket" "initial_bucket" {
  bucket = "${var.app_name}-initial-bucket"
}

resource "aws_s3_bucket_ownership_controls" "initial_bucket_ownership_control" {
  bucket = aws_s3_bucket.initial_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "initial_bucket_acl" {
  depends_on = [aws_s3_bucket_ownership_controls.initial_bucket_ownership_control]

  bucket = aws_s3_bucket.initial_bucket.id
  acl    = "private"
}

resource "aws_s3_bucket" "test_bucket" {
  bucket = "${var.app_name}-test-bucket"
}

resource "aws_s3_bucket_ownership_controls" "test_bucket_ownership_control" {
  bucket = aws_s3_bucket.test_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "test_bucket_acl" {
  depends_on = [aws_s3_bucket_ownership_controls.test_bucket_ownership_control]

  bucket = aws_s3_bucket.test_bucket.id
  acl    = "private"
}


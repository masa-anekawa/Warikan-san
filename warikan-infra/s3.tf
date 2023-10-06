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

resource "aws_s3_bucket" "confirmed_bucket" {
  bucket = "${var.app_name}-confirmed-bucket"
}

resource "aws_s3_bucket_ownership_controls" "confirmed_bucket_ownership_control" {
  bucket = aws_s3_bucket.confirmed_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "confirmed_bucket_acl" {
  depends_on = [aws_s3_bucket_ownership_controls.confirmed_bucket_ownership_control]

  bucket = aws_s3_bucket.confirmed_bucket.id
  acl    = "private"
}


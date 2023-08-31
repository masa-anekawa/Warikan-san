resource "aws_s3_bucket" "inital_bucket" {
  bucket = "${var.app_name}-initial-bucket"
}

resource "aws_s3_bucket_ownership_controls" "input_bucket_ownership_control" {
  bucket = aws_s3_bucket.inital_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "input_bucket_acl" {
  depends_on = [aws_s3_bucket_ownership_controls.input_bucket_ownership_control]

  bucket = aws_s3_bucket.inital_bucket.id
  acl    = "private"
}


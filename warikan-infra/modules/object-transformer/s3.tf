resource "aws_s3_bucket" "output_bucket" {
  bucket = "${var.project_name}-${var.name}-outputs"
}

resource "aws_s3_bucket_ownership_controls" "output_bucket_ownership_control" {
  bucket = aws_s3_bucket.output_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "output_bucket_acl" {
  depends_on = [aws_s3_bucket_ownership_controls.output_bucket_ownership_control]

  bucket = aws_s3_bucket.output_bucket.id
  acl    = "private"
}

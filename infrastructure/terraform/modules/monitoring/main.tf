# ─── Monitoring Module ───
# Deploys Prometheus + Grafana on EKS via Helm

variable "environment" { type = string }
variable "project_name" { type = string }
variable "vpc_id" { type = string }
variable "subnet_ids" { type = list(string) }
variable "eks_cluster_endpoint" { type = string }
variable "eks_cluster_name" { type = string }

# ECR Repository for application images
resource "aws_ecr_repository" "app" {
  name                 = "${var.project_name}/${var.environment}"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-ecr"
    Environment = var.environment
  }
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "app" {
  name              = "/aws/eks/${var.eks_cluster_name}/app"
  retention_in_days = var.environment == "production" ? 90 : 30

  tags = {
    Environment = var.environment
  }
}

# S3 Bucket for backups/logs
resource "aws_s3_bucket" "app_data" {
  bucket = "${var.project_name}-${var.environment}-data-${random_id.suffix.hex}"

  tags = {
    Environment = var.environment
  }
}

resource "random_id" "suffix" {
  byte_length = 4
}

resource "aws_s3_bucket_versioning" "app_data" {
  bucket = aws_s3_bucket.app_data.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "app_data" {
  bucket = aws_s3_bucket.app_data.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Outputs
output "ecr_repository_url" { value = aws_ecr_repository.app.repository_url }
output "grafana_endpoint" { value = "http://grafana.monitoring.svc.cluster.local" }
output "prometheus_endpoint" { value = "http://prometheus.monitoring.svc.cluster.local" }
output "s3_bucket_name" { value = aws_s3_bucket.app_data.id }

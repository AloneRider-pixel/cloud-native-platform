# ─── VPC Outputs ───
output "vpc_id" {
  value = module.vpc.vpc_id
}

output "private_subnet_ids" {
  value = module.vpc.private_subnet_ids
}

output "public_subnet_ids" {
  value = module.vpc.public_subnet_ids
}

# ─── EKS Outputs ───
output "eks_cluster_name" {
  value = module.eks.cluster_name
}

output "eks_cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "eks_cluster_ca" {
  value = module.eks.cluster_ca
}

output "kubeconfig_command" {
  value = "aws eks update-kubeconfig --name ${module.eks.cluster_name} --region ${var.aws_region}"
}

# ─── RDS Outputs ───
output "rds_endpoint" {
  value     = module.rds.endpoint
  sensitive = true
}

output "rds_port" {
  value = module.rds.port
}

# ─── Redis Outputs ───
output "redis_endpoint" {
  value     = module.redis.endpoint
  sensitive = true
}

output "redis_port" {
  value = module.redis.port
}

# ─── Monitoring Outputs ───
output "grafana_endpoint" {
  value = module.monitoring.grafana_endpoint
}

output "prometheus_endpoint" {
  value = module.monitoring.prometheus_endpoint
}

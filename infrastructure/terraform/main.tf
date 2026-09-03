# ─── Main Terraform Configuration ───
# Provisions complete AWS infrastructure for cloud-native application

# ─── VPC ───
module "vpc" {
  source = "./modules/vpc"

  environment  = var.environment
  project_name = var.project_name
  vpc_cidr     = var.vpc_cidr
  azs          = var.availability_zones
}

# ─── EKS Cluster ───
module "eks" {
  source = "./modules/eks"

  environment        = var.environment
  project_name       = var.project_name
  cluster_name       = "${var.project_name}-${var.environment}"
  vpc_id             = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids
  node_instance_type = var.eks_node_instance_type
  node_desired_size  = var.eks_node_desired_size
  node_min_size      = var.eks_node_min_size
  node_max_size      = var.eks_node_max_size
  kubernetes_version = var.kubernetes_version
}

# ─── RDS PostgreSQL ───
module "rds" {
  source = "./modules/rds"

  environment        = var.environment
  project_name       = var.project_name
  vpc_id             = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids
  instance_class     = var.rds_instance_class
  allocated_storage  = var.rds_allocated_storage
  db_name            = var.db_name
  db_username        = var.db_username
}

# ─── ElastiCache Redis ───
module "redis" {
  source = "./modules/redis"

  environment        = var.environment
  project_name       = var.project_name
  vpc_id             = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids
  node_type          = var.redis_node_type
  num_cache_nodes    = var.redis_num_nodes
}

# ─── Monitoring Stack ───
module "monitoring" {
  source = "./modules/monitoring"

  environment  = var.environment
  project_name = var.project_name
  vpc_id       = module.vpc.vpc_id
  subnet_ids   = module.vpc.private_subnet_ids

  eks_cluster_endpoint = module.eks.cluster_endpoint
  eks_cluster_name     = module.eks.cluster_name
}

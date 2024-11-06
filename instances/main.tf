terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "us-east-1"
}

# Módulo para o servidor web
module "legacy_server" {
  source            = "./modules/legacy_server"
  ami               = var.ami
  instance_type     = var.legacy_server_instance_type
  env               = var.env
  key_name          = var.key_name
  private_key_path  = var.private_key_path
  monitoring_files_path = "./monitoring"
}

module "sites_server" {
  source            = "./modules/sites_server"
  ami               = var.ami
  instance_type     = var.sites_server_instance_type
  env               = var.env
  key_name          = var.key_name
  private_key_path  = var.private_key_path
  monitoring_files_path = "./monitoring"
}

# Módulo para o servidor de banco de dados
# module "db_server" {
#   source             = "./modules/db_server"
#   ami_id             = var.db_server_ami_id
#   instance_type      = var.db_server_instance_type
#   key_name           = var.key_name
#   instance_name      = "db-server-${var.env}"
#   private_key_path   = var.private_key_path
# }
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"

  backend "s3" {
    # Replace this with your bucket name!
    bucket         = "bonde-terraform-up-and-running-state"
    key            = "global/s3/terraform.tfstate"
    region         = "us-east-1"

    # Replace this with your DynamoDB table name!
    dynamodb_table = "terraform-up-and-running-locks"
    encrypt        = true
  }
}

provider "aws" {
  region    = "us-east-1"
}

# Módulo para o servidor web
module "legacy_server" {
  source            = "./modules/common"
  ami               = var.ami
  instance_type     = var.legacy_server_instance_type
  instance_name     = "legacy-server-${var.env}"
  key_name          = var.key_name
  private_key_path  = var.private_key_path
  monitoring_files_path = "./monitoring"
}

module "sites_server" {
  source            = "./modules/common"
  ami               = var.ami
  instance_type     = var.sites_server_instance_type
  instance_name     = "sites-server-${var.env}"
  key_name          = var.key_name
  private_key_path  = var.private_key_path
  monitoring_files_path = "./monitoring"
}
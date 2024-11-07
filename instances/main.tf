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

locals {
  # Tipo de imagem para o servidor legado (APIS e Clientes Bonde)
  ami                         = "ami-0866a3c8686eaeeba"

  # Nome da chave SSH
  key_name                    = "custom-host"

  # Caminho para a chave privada SSH
  private_key_path            = "~/.ssh/ailton-krenak.pem"

  # Ambiente (dev, staging, production)
  env                         = terraform.workspace

  # Tipo de instância para o servidor legado (APIS e Clientes Bonde)
  legacy_server_instance_type = terraform.workspace == "stage" ? "t3.small" : "t3.micro"

  # Tipo de instância para o servidor de sites (Bonde Público e CMS)
  sites_server_instance_type  = terraform.workspace == "stage" ? "t3.micro" : "t2.micro"
}

# Módulo para o servidor web
module "legacy_server" {
  source            = "./modules/common"
  ami               = local.ami
  instance_type     = local.legacy_server_instance_type
  instance_name     = "legacy-server-${local.env}"
  key_name          = local.key_name
  private_key_path  = local.private_key_path
  monitoring_files_path = "./monitoring"
}

module "sites_server" {
  source            = "./modules/common"
  ami               = local.ami
  instance_type     = local.sites_server_instance_type
  instance_name     = "sites-server-${local.env}"
  key_name          = local.key_name
  private_key_path  = local.private_key_path
  monitoring_files_path = "./monitoring"
}
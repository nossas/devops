module "common" {
  source            = "../common"
  ami               = var.ami
  instance_type     = var.instance_type
  instance_name     = "sites-server-${var.env}"
  key_name          = var.key_name
  private_key_path  = var.private_key_path
  monitoring_files_path = var.monitoring_files_path
}

resource "aws_instance" "sites_server" {
    ami = var.ami
    instance_type = var.instance_type
    
    depends_on = [ module.common ]
}
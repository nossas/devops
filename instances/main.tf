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

resource "aws_key_pair" "devops_key_pair" {
  key_name   = "devops-host"
  public_key = file("~/.ssh/id_rsa.pub")
}

resource "aws_instance" "legacy_server" {
  ami           = "ami-0866a3c8686eaeeba"
  instance_type = "t2.micro"

  key_name = aws_key_pair.devops_key_pair.key_name

  tags = {
    Name = "legacy-server"
  }

  provisioner "file" {
    # Copia arquivos para configuração do monitoramento
    source      = "./monitoring"
    destination = "/home/ubuntu/monitoring"

    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("~/.ssh/id_rsa")
      host        = self.public_ip
    }
  }

  provisioner "remote-exec" {
    inline = [
      "sudo apt-get update -y",
      "sudo apt-get install -y docker.io",
      "sudo systemctl start docker",
      "sudo systemctl enable docker",
      "sudo usermod -aG docker ubuntu",
      # Altera o hostname antes de instalar o telegraf  
      "sudo hostnamectl set-hostname --transient --static legacy-server",
      # Inicia a configuração do monitoramento
      "cd /home/ubuntu/monitoring/",
      "sudo chmod +x install-telegraf.sh",
      "sudo ./install-telegraf.sh"
    ]

    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("~/.ssh/id_rsa")
      host        = self.public_ip
    }
  }
}

output "instance_public_ip" {
  value       = aws_instance.legacy_server.public_ip
  description = "Endereço IP público da instância"
}
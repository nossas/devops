# Define um formato de instância genérica para criar novas instâncias monitoradas
# e habilitadas para implantar arquiteturas baseadas em Docker.

resource "aws_instance" "server" {
  # Sistema operacional na Amazon
  ami           = var.ami
  instance_type = var.instance_type

  key_name = var.key_name

  tags = {
    Name = var.instance_name
  }

  provisioner "file" {
    # Copia arquivos para configuração do monitoramento
    source      = var.monitoring_files_path
    destination = "/home/ubuntu/monitoring"

    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file(var.private_key_path)
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
      "sudo hostnamectl set-hostname --transient --static ${var.instance_name}",
      # Inicia a configuração do monitoramento
      "cd /home/ubuntu/monitoring/",
      "sudo chmod +x install-telegraf.sh",
      "sudo ./install-telegraf.sh"
    ]

    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file(var.private_key_path)
      host        = self.public_ip
    }
  }
}
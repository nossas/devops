# Define um formato de instância genérica para criar novas instâncias monitoradas
# e habilitadas para implantar arquiteturas baseadas em Docker.

resource "aws_instance" "server" {
  # Sistema operacional na Amazon
  ami           = var.ami
  instance_type = var.instance_type

  # Nome da chave existente na Amazon, você deve ter o par da chave na sua máquina
  key_name = var.key_name

  tags = {
    Name = var.instance_name
  }

  root_block_device {
    # Aumente para o tamanho necessário em GB
    volume_size = var.volume_size
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
      "sudo ./install-telegraf.sh",
      # Configura a variável que será usada no telegraf
      "sudo su -c 'echo \"INFLUXDB_TOKEN=${var.influxdb_token}\" >> /etc/default/telegraf'",
      # Reinicia o telegraf para garantir que a variavel está configurada
      "sudo systemctl restart telegraf",
      # Adiciona essa instância ao Portainer
      "sudo docker run -d -v /var/run/docker.sock:/var/run/docker.sock -v /var/lib/docker/volumes:/var/lib/docker/volumes -v /:/host -v portainer_agent_data:/data --restart always -e EDGE=1 -e EDGE_ID=${var.portainer_edge_id} -e EDGE_KEY=${var.portainer_edge_key} -e EDGE_INSECURE_POLL=1 --name portainer_edge_agent portainer/agent:2.27.3"
    ]

    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file(var.private_key_path)
      host        = self.public_ip
    }
  }
}

resource "aws_eip_association" "eip_assoc" {
  count         = var.elastic_ip_allocation_id != "" ? 1 : 0
  instance_id   = aws_instance.server.id
  allocation_id = var.elastic_ip_allocation_id
}
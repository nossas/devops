# creating ec2 instance :
resource "aws_instance" "ec2" {
  ami           = data.aws_ami.ubuntu_ami.id
  instance_type = "t2.micro"
  # user_data     = data.template_cloudinit_config.user_data.rendered
  key_name = "Chave DEV"

  provisioner "file" {
    source      = "./application/"
    destination = "/home/ubuntu/"

    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file(var.key_file)
      host        = self.public_dns
    }
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x install.sh",
      "./install.sh",
      "cd public",
      "nohup sudo /home/ubuntu/.deno/bin/deno run --allow-net --allow-read index.ts &",
      "sleep 1"
    ]

    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file(var.key_file)
      host        = self.public_dns
    }
  }

  tags = merge(local.tags, {
    Name = var.instance_name
  })
}

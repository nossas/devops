variable ami {
    description = "Tipo de imagem para o servidor legado (APIS e Clientes Bonde)"
    type        = string
    default     = "ami-0866a3c8686eaeeba"
}

variable "legacy_server_instance_type" {
    description = "Tipo de instância para o servidor legado (APIS e Clientes Bonde)"
    type        = string
    default     = "t2.micro"
}

variable "sites_server_instance_type" {
    description = "Tipo de instância para o servidor de sites (Bonde Público e CMS)"
    type        = string
    default     = "t2.micro"
}

variable "env" {
    description = "Ambiente (dev, staging, production)"
    type        = string
}

variable "key_name" {
    description = "Nome da chave SSH"
    type        = string
}

variable "private_key_path" {
    description = "Caminho para a chave privada SSH"
    type        = string
}
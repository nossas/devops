variable ami {
    description = "Tipo de imagem para o servidor de sites (APIS e Clientes Bonde)"
    type        = string
}

variable "instance_type" {
    description = "Tipo de instância para o servidor legado (APIS e Clientes Bonde)"
    type        = string
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

variable "monitoring_files_path" {
    description = "Caminho para arquivos de instalação do monitoramento"
    type        = string
}
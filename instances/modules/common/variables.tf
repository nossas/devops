variable ami {
    description = "Tipo de imagem para o servidor legado (APIS e Clientes Bonde)"
    type        = string
}

variable "instance_type" {
    description = "Tipo de instância"
    type        = string
}

variable "instance_name" {
    description = "Nome da instância"
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
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

variable "influxdb_token" {
    description = "Chave utilizada para o telegraf enviar dados ao Influxdb"
    type        = string
    sensitive   = true
}

variable "elastic_ip_allocation_id" {
    description = "ID da alocação de um IP Elástico da AWS"
    type        = string
    default     = ""
}

variable "portainer_edge_id" {
    description = "ID do ambiente no Portainer"
    type        = string
}

variable "portainer_edge_key" {
    description = "Chave Secreta do ambiente no Portainer"
    type        = string
    sensitive   = true
}

variable "volume_size" {
    description = "Tamanho em GB do volume da instância"
    type        = number
}
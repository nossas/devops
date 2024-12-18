variable "influxdb_token" {
    description = "Chave utilizada para o telegraf enviar dados ao Influxdb"
    type        = string
    sensitive   = true
}

variable "legacy_elastic_ip_allocation_id" {
    description = "ID da alocação de um IP Elástico da AWS"
    type        = string
    default     = ""
}

variable "sites_elastic_ip_allocation_id" {
    description = "ID da alocação de um IP Elástico da AWS"
    type        = string
    default     = ""
}

variable "ami" {
    description = "Tipo de imagem para o servidor legado (APIS e Clientes Bonde)"
    type        = string
    # Ubuntu x86, caso você mude o AMI lembre de mudar o tipo da instância
    default     = "ami-0866a3c8686eaeeba"
}

variable "legacy_server_instance_type" {
    description = "Tipo de instância para o servidor legado (APIS e Clientes Bonde)"
    type        = string
    # Arch x86, caso você mude a arquitetura da instância lembre de mudar o AMI
    default     = "t3.micro"
}

variable "sites_server_instance_type" {
    description = "Tipo de instância para o servidor de sites (Bonde Público e CMS)"
    type        = string
    default     = "t3.micro"
}

variable "legacy_portainer_edge_id" {
    description = "ID do ambiente no Portainer"
    type        = string
}

variable "legacy_portainer_edge_key" {
    description = "Chave Secreta do ambiente no Portainer"
    type        = string
    sensitive   = true
}

variable "sites_portainer_edge_id" {
    description = "ID do ambiente no Portainer"
    type        = string
}

variable "sites_portainer_edge_key" {
    description = "Chave Secreta do ambiente no Portainer"
    type        = string
    sensitive   = true
}
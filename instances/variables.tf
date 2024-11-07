variable "influxdb_token" {
    description = "Chave utilizada para o telegraf enviar dados ao Influxdb"
    type        = string
    sensitive   = true
}
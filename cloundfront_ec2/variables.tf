variable "region" {
  type        = string
  description = "The AWS Region to use"
  default     = "us-east-1"
}

variable "domain_name" {
  type        = string
  description = "The domain name to use"
  default     = "nossastech.org"
}

variable "instance_name" {
  type        = string
  description = "The instance name to use"
  default     = "ec2-cloudfront"
}

variable "key_file" {
  type = string
  description = "The private key file to use"
  default = "~/Documents/NOSSAS/Chave DEV.pem"
}
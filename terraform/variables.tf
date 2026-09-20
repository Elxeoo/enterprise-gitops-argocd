variable "location" {
  default = "swedencentral"
  type    = string
}

variable "resource_group_name" {
  default = "rg-enterprise-gitops"
  type    = string
}

variable "vnet_cidr" {
  default = "10.220.0.0/16"
  type    = string
}

variable "subnet_cidr" {
  default = "10.220.1.0/24"
  type    = string
}

variable "acr_name" {
  default = "acrenterprisecan01"
  type    = string
}

variable "aks_cluster_name" {
  default = "aks-gitops-cluster"
  type    = string
}
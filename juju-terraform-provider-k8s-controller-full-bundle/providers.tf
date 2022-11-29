# This ones will be downloaded on `terraform init`
terraform {
  required_providers {
    juju = {
      version = "~> 0.4.3"
      source  = "juju/juju"
    }
  }
}


# Provider configuration section. 
# See: https://registry.terraform.io/providers/juju/juju/latest/docs#schema
provider "juju" {}
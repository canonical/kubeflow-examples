# Kubeflow on baremetal K8s cluster example

1. Have an existing K8s cluster and a juju controller attached to said cluster.
2. Run `terraform init` inside this folder.
3. Create a `terraform.tfvars` following the example structure of `terraform.tfvars.example`.
4. Run `terraform apply`.
5. Watch the deployment work and stabilize inside the juju controller and model defined in the vars.
6. Enjoy

## TLDR

```bash
terraform init && terraform apply
```

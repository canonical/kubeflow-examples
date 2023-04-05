#!/bin/bash

sudo snap install microk8s --classic --channel=1.22/stable
sudo usermod -a -G microk8s $USER
newgrp microk8s

sudo snap install kubectl
mkdir -p ~/.kube
microk8s config > ~/.kube/config
sudo chown -f -R $USER ~/.kube

microk8s enable gpu
microk8s enable registry:size=40Gi

microk8s enable dns storage ingress metallb:10.64.140.43-10.64.140.49
microk8s status --wait-ready

rm -Rf ~/.local/share/juju/
sudo snap install juju --classic

juju bootstrap microk8s micro
juju add-model kubeflow

juju deploy kubeflow-lite --trust

juju config oidc-gatekeeper public-url=http://10.64.140.43.nip.io
juju config dex-auth public-url=http://10.64.140.43.nip.io static-username=admin static-password=admin
juju config minio secret-key=minio123 access-key=minio123

watch -c juju status --color


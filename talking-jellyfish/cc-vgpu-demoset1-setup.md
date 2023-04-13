# Instruction how to setup the demo on Canonical VGPU demo1

## Install OS

Install Ubuntu Desktop 22.04 on one of the drives. Check the order of starting if the PXE boot is first then machine will start for a long time.

Enable the SSH access by importing the launchpad ssh keys
```shell
ssh-import-id <launchpad-id>
```

## Install GPU

Install the gpu drivers and restart the machine
```shell
sudo apt install ubuntu-drivers-common -y
sudo ubuntu-drivers install --gpgpu
sudo apt install nvidia-utils-470-server -y

sudo reboot
```

## Get demo codes

Install Git 
```shell
sudo apt install git
```

Clone AI/ML demos repository
```shell
git clone https://github.com/canonical/ai-ml-demos.git
```

Go to the jellyfish demo folder
```shell
cd ai-ml-demos/talking-jellyfish/
```

## Prepare environment

Install Microk8s and kubectl
```shell
sudo snap install kubectl --classic

sudo snap install microk8s --channel 1.24/stable --classic
sudo usermod -a -G microk8s ubuntu
sudo chown -f -R ubuntu ~/.kube
newgrp microk8s
```

Config k8s cluster access
```shell
mkdir -p ~/.kube
microk8s config > ~/.kube/config
```

Install and bootstrap juju
```shell
sudo snap install juju --classic

microk8s enable gpu dns hostpath-storage ingress metallb:10.64.140.43-10.64.140.49
juju bootstrap microk8s micro
```

Setup kubeflow for inference
```shell
juju add-model kubeflow
juju deploy seldon-core seldon-controller-manager --channel 1.14/stable
```

## Deploy models

Deploy models using ready-made images or create your own, use README in models:
- chatbot
- object-detection

## Install Applications

Follow the main README section about application installation.


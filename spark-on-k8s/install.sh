#!/bin/bash

#TODO install microk8s

alias kubectl="microk8s kubectl"

#setup juju
sudo snap install juju --classic
juju bootstrap microk8s micro
juju add-model kubeflow

#deploy spark
juju deploy spark-k8s
kubectl get all -n kubeflow

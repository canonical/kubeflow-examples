# Charmed Kubeflow + mindspore showcase

This is a demo for Charmed Kubeflow mindspore integration

## Create a cloud instance
any instance on AWS/GCP/Azure with minimum 16G or RAM, 4vCPU and 400GB of disk is enough

## SSH to your instance

## Install Charmed Kubeflow
using the quickstart guide from : https://charmed-kubeflow.io/docs/quickstart

## Bump up the notebooks version to have mindspore integration available
`juju refresh jupyter-ui --channel=latest/edge`

## Create a notebook instance
when choosing the notebook image choose mindspore one

## Use mindspore.ipynb notebook
pull this repo to the notebook server

`git clone git@github.com:canonical/ai-ml-demos.git`

## Demo description
notebook contains steps of downloading the dataset, training the model
it requires python 3.9 or above
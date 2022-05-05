# Data Drift - prepare environment

## Tools setup

Install microk8s

```
sudo snap install microk8s --classic --channel=1.21/stable

#change username
sudo usermod -a -G microk8s ubuntu
sudo chown -f -R ubuntu ~/.kube
newgrp microk8s

sudo microk8s enable dns storage ingress registry rbac metallb:10.64.140.43-10.64.140.49,192.168.0.105-192.168.0.111
```

Install and bootstrap juju

```
sudo snap install juju --classic
juju bootstrap microk8s micro
```

Install kubectl

```
sudo snap install kubectl --classic
microk8s config > ~/.kube/config
```

Install kn CLI

```
#works for linux only
wget https://github.com/knative/client/releases/download/knative-v1.3.1/kn-linux-amd64 -O kn
chmod +x kn
sudo mv kn /usr/local/bin
```

## Install KNative

Install istio

First time only

```
#optional
curl -sL https://istio.io/downloadIstioctl | sh -
export PATH=$PATH:$HOME/.istioctl/bin
istioctl x precheck
```

Install istio using istioctl

```
#install
istioctl install -y
kubectl get svc -nistio-system
```

Deploy knative operator

```
kubectl config set-context --current --namespace=default
kubectl apply -f https://github.com/knative/operator/releases/download/knative-v1.3.1/operator.yaml
```

Deploy knative serving

```
kubectl apply -f https://raw.githubusercontent.com/Barteus/kubeflow-examples/main/knative-example/crd-serving.yaml
```

DNS

```
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.3.0/serving-default-domain.yaml
```

Istio config

```
kubectl apply -f https://raw.githubusercontent.com/Barteus/kubeflow-examples/main/knative-example/istio-config.yaml
```

Install eventing

```
kubectl apply -f https://raw.githubusercontent.com/Barteus/kubeflow-examples/main/knative-example/crd-eventing.yaml
```

## Install Seldon, Minio, MLFlow

Deploy bundle

````
juju add-model kubeflow
juju deploy ./kubeflow-examples/data-drift/bundle.yaml
````

# Data drift detection

## Train datadrift model

Run notebook `data-drift-training.ipynb`. Take the model URI - you will need it
in the next notebook.

## Deploy pipeline with data drift step

In the notebook `e2e-pipeline-drift.ipynb` change the model URI in the data
drift detection method to the one from previous step. Run the notebook to deploy
the pipeline

Run the pipeline twice with parameters:

- https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv
- https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-white.csv

For Red Wine dataset there is no drift, for White Wine dataset the data drift is
detected.


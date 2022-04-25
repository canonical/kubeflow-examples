# Data Drift

Deploy bundle

````
juju deploy ./kubeflow-examples/data-drift/bundle.yaml
````

Deploy knative

```
kubectl config set-context --current --namespace=default
kubectl apply -f https://github.com/knative/operator/releases/download/knative-v1.3.1/operator.yaml
```

Install istio

Only first time

```
#optional
curl -sL https://istio.io/downloadIstioctl | sh -
export PATH=$PATH:$HOME/.istioctl/bin
istioctl x precheck
```

Required

```
#install
istioctl install -y
kubectl get svc -nistio-system
```

DNS

```
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.3.0/serving-default-domain.yaml
```

## Install eventing

Install eventing

```
kubectl apply -f crd-eventing.yaml
```

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


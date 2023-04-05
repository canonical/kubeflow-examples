# Deploy model on the edge with Microk8s, Seldon and Istio 

## Setup environemnt

Create t2.medium instance with public IP. 

## Prepare environment

Install microk8s

```shell
sudo snap install microk8s --channel 1.24/stable --classic
sudo usermod -a -G microk8s ubuntu
mkdir -p ~/.kube
sudo chown -f -R ubuntu ~/.kube
newgrp microk8s

microk8s enable hostpath-storage dns ingress
```

Result
```shell
$ microk8s status
microk8s is running
high-availability: no
  datastore master nodes: 127.0.0.1:19001
  datastore standby nodes: none
addons:
  enabled:
    dns                  # (core) CoreDNS
    ha-cluster           # (core) Configure high availability on the current node
    hostpath-storage     # (core) Storage class; allocates storage from host directory
    ingress              # (core) Ingress controller for external access
    storage              # (core) Alias to hostpath-storage add-on, deprecated
  disabled:
    community            # (core) The community addons repository
    dashboard            # (core) The Kubernetes dashboard
    gpu                  # (core) Automatic enablement of Nvidia CUDA
    helm                 # (core) Helm 2 - the package manager for Kubernetes
    helm3                # (core) Helm 3 - Kubernetes package manager
    host-access          # (core) Allow Pods connecting to Host services smoothly
    mayastor             # (core) OpenEBS MayaStor
    metallb              # (core) Loadbalancer for your Kubernetes cluster
    metrics-server       # (core) K8s Metrics Server for API access to service metrics
    prometheus           # (core) Prometheus operator for monitoring and logging
    rbac                 # (core) Role-Based Access Control for authorisation
    registry             # (core) Private image registry exposed on localhost:32000
```

Install juju and bootstrap controller
```shell
sudo snap install juju --classic
juju bootstrap microk8s micro
juju add-model kubeflow
```

Deploy bundle
```shell
juju deploy ./bundle.yaml
```

Result exposed istio-gateway-workload
```shell
$ microk8s.kubectl get svc -n kubeflow
NAME                                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                                 AGE
modeloperator                        ClusterIP   10.152.183.248   <none>        17071/TCP                               72m
istio-gateway                        ClusterIP   10.152.183.119   <none>        65535/TCP                               29m
istio-gateway-endpoints              ClusterIP   None             <none>        <none>                                  29m
istio-pilot                          ClusterIP   10.152.183.254   <none>        65535/TCP                               27m
istio-pilot-endpoints                ClusterIP   None             <none>        <none>                                  27m
istiod                               ClusterIP   10.152.183.156   <none>        15010/TCP,15012/TCP,443/TCP,15014/TCP   27m
istio-ingressgateway-workload        NodePort    10.152.183.183   <none>        80:31788/TCP,443:32475/TCP              26m
seldon-controller-manager-operator   ClusterIP   10.152.183.179   <none>        30666/TCP                               26m
seldon-controller-manager            ClusterIP   10.152.183.133   <none>        8080/TCP,4443/TCP                       25m
seldon-webhook-service               ClusterIP   10.152.183.223   <none>        4443/TCP                                24m
```

## Deploy and expose model

Deploy Seldon Model

```shell
microk8s.kubectl apply -f - << END
apiVersion: machinelearning.seldon.io/v1
kind: SeldonDeployment
metadata:
  name: seldon-deployment-example
spec:
  name: sklearn-iris-deployment
  predictors:
  - componentSpecs:
    - spec:
        containers:
        - image: seldonio/sklearn-iris:0.3
          imagePullPolicy: IfNotPresent
          name: sklearn-iris-classifier
    graph:
      children: []
      endpoint:
        type: REST
      name: sklearn-iris-classifier
      type: MODEL
    name: default
    replicas: 1
END
```

Expose using Istio Virtual Service

```shell
microk8s.kubectl apply -f - << END
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: iris-server
  namespace: default
spec:
  gateways:
    - kubeflow/kubeflow-gateway
  hosts:
    - '*'
  http:
    - match:
        - uri:
            prefix: /model/iris/
      rewrite:
        uri: /
      route:
        - destination:
            host: seldon-deployment-example-default.default.svc.cluster.local
            port:
              number: 8000
END
```

## Call model

Build the URL for the exposed model:
1. Get public IP for the EC2 instance
2. Get the port on which Service is exposed 
```shell
ubuntu@ip-172-31-2-238:~$ microk8s.kubectl get svc istio-ingressgateway-workload -n kubeflow
NAME                                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                                 AGE
istio-ingressgateway-workload        NodePort    10.152.183.183   <none>        80:31788/TCP,443:32475/TCP              26m
```

```shell
$ curl  -s http://34.243.192.192:30380/model/iris/api/v0.1/predictions  \
  -H "Content-Type: application/json"  \
  -d '{"data":{"ndarray":[[5.964,4.006,2.081,1.031]]}}'
{"data":{"names":["t:0","t:1","t:2"],"ndarray":[[0.9548873249364059,0.04505474761562512,5.7927447968953825e-05]]},"meta":{"requestPath":{"sklearn-iris-classifier":"seldonio/sklearn-iris:0.3"}}}
```
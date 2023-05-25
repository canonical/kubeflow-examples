# Run Kubeflow Pipeline on EKS spot instance

Start by create a EKS cluster and deploy Kubeflow on top of it.

Add spot instances using eksctl

```
eksctl create nodegroup --cluster=<cluster_name> --spot --instance-types=p3.2xlarge,g4dn.xlarge --name gpu-spot --nodes 1
kubectl taint nodes <node1> spot-instance=true:PreferNoSchedule
kubectl get nodes -o custom-columns=NAME:.metadata.name,TAINTS:.spec.taints --no-headers
```

Run the examples 02 and 03.

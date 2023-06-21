# EKS Cluster setup
This folder contains eksctl cluster config which can be used to deploy Charmed Kubeflow/ Charmed mlflow (?). 
For information about deploying Charmed Mlflow, please refer to [this guide](https://discourse.charmhub.io/t/deploying-charmed-mlflow-v2-to-eks/10913).

The cluster config has some preset values which you might want to check before deploying. e.g.:
* The cluster will be deployed by default to `eu-central-1` zone. Feel free to edit `metadata.region` and `availabilityZones` according to your needs.
* The cluster will be deployed with `t2.2xlarge` ec2 instance types for worker nodes. Feel free to edit `managedNodeGroups[0].instanceType`.
* Each worker node will have gp2 disk of size 100Gb. Feel free to edit `managedNodeGroups[0].volumeSize`.
* By default this template will enable you to ssh into ec2 worker nodes with ssh key `dektop-eu-central-1` the key must exist before cluster creation and it also has to be in the same zone as the cluster (inn this case `dektop-eu-central-1`). You can change the key name under `managedNodeGroups[0].ssh.publicKeyName` to any key you have.
* This cluster will have 2 worker nodes. Feel free to edit the `maxSize` and `minSize` under `managedNodeGroups[0]` according to your needs.

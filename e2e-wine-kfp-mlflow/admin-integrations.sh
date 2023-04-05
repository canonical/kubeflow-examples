#!/bin/bash

USER_NAMESPACE=admin

#MLflow
cat <<EOF | kubectl create -n $USER_NAMESPACE -f -
apiVersion: kubeflow.org/v1alpha1
kind: PodDefault
metadata:
  name: mlflow-server-minio
spec:
  desc: Allow access to MLFlow
  env:
  - name: MLFLOW_S3_ENDPOINT_URL
    value: http://minio.kubeflow:9000
  - name: MLFLOW_TRACKING_URI
    value: http://mlflow-server.kubeflow.svc.cluster.local:5000
  selector:
    matchLabels:
      mlflow-server-minio: "true"
EOF

cat <<EOF | kubectl create -n $USER_NAMESPACE -f -
apiVersion: kubeflow.org/v1alpha1
kind: PodDefault
metadata:
 name: access-minio
spec:
 desc: Allow access to Minio
 selector:
   matchLabels:
     access-minio: "true"
 env:
   - name: AWS_ACCESS_KEY_ID
     valueFrom:
       secretKeyRef:
         name: mlpipeline-minio-artifact
         key: accesskey
         optional: false
   - name: AWS_SECRET_ACCESS_KEY
     valueFrom:
       secretKeyRef:
         name: mlpipeline-minio-artifact
         key: secretkey
         optional: false
   - name: MINIO_ENDPOINT_URL
     value: http://minio.kubeflow.svc.cluster.local:9000
EOF

kubectl get secret mlflow-server-seldon-init-container-s3-credentials --namespace=kubeflow -o yaml \
  | sed "s/namespace: kubeflow/namespace: $USER_NAMESPACE/" \
  | sed 's/name: mlflow-server-seldon-init-container-s3-credentials/name: seldon-init-container-secret/g' \
  | kubectl apply -n $USER_NAMESPACE -f -

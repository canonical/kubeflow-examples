# Build step using the docker image

Created based on: https://www.kubeflow.org/docs/components/pipelines/sdk/component-development/#writing-your-component-definition-file

Some manual interaction will be needed. Login by default is using the dockerhub.

```
sudo docker login
sudo docker build . -t bponieckiklotz/kubeflow-e2e-seldon-mlflow-deploy-step:0.1
sudo docker push bponieckiklotz/kubeflow-e2e-seldon-mlflow-deploy-step:0.1
```
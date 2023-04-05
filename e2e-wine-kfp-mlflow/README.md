# E2E pipeline

## Notebook

The `e2e-kfp-mlflow-seldon-pipeline` notebook contains the simplified
implementation of same functionality pipeline as `pipeline.py`.

Notebook shows the end-to-end process of developing and execution of pipeline
steps locally and in the working Kubeflow installation.

## Build the components using your image registry

Go to each of the components and use `build_image.sh` to have own image. Update
the value of component.yaml file with new image.

## Build pipeline

Run the `pipeline.py` script. The generated pipeline will be in the `generated`
folder

## Run pipeline

1. Upload the pipeline using the UI
2. Start a run, use for the `url` parameter
   use: `https://raw.githubusercontent.com/Barteus/kubeflow-examples/main/e2e-wine-kfp-mlflow/winequality-red.csv`
3. Use kubectl port-forward to connect to service and `sample-prediction.sh` as
   an example call.

## Techniques to define tasks

1. Function based
2. Docker image based
3. Reuse of existing component from kfp repository
# Resources

## Files
- `ml-workflow-demo-kfp-katib-mlflow.ipynb` Jupyter notebook with all pipeline steps of the demo.
- `Dockerfile` Specifies Docker image that was used with this demo.
- `ml-workflow-demo-tf-train-model.py` Python script that was used to build image for this demo.
- `requirements.txt` Dependencies for this demo.

## Build Tensorflow training Docker image

To build a modified Tensorflow training image modify `ml-workflow-demo-tf-train-model.py` as required. Build Docker conainer using your own credentials:

```
docker build -t <your_acc>/kubeflow-training:latest .
```

Push image to Docker registry:

```
 docker push <your_acc>/kubeflow-training:latest
```

Replace image URI in pipeline.

## Modifying Jupyter notebook

If modifying Jupyter notebook that describes pipeline for this demo `ml-workflow-demo-tf-train-model.py`, before commit run the following command to remove all output of the execution:

```
jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace ml-workflow-demo-tf-train-model.py
```

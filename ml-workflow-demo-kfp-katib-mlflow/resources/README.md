# Resources

## Files

- `ml-workflow-demo-kfp-katib-mlflow.ipynb` Jupyter notebook with all pipeline steps of the demo, all graphics, and diagrams.
- `resources/Dockerfile` Specifies Docker image that was used with this demo.
- `resources/requirements.txt` Dependencies for this demo.

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

If modifying Jupyter notebook that describes pipeline for this demo `ml-workflow-demo-tf-train-model.ipnyb`, before commit run the following command to remove all output of the execution:

```
jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace ml-workflow-demo-tf-train-model.ipynb`
```

## Convert Jupyter notebook into markdown guide

To convert Jupyter notebook to markdown guide:
```
jupyter nbconvert --to markdown ml-workflow-demo-kfp-katib-mlflow.ipynb
```

Markdown file will be created: `ml-workflow-demo-kfp-katib-mlflow.md`. This markdown version should be used as a guide. `README.md` in main directory is produced this way, eg. `jupyter nbconvert --to markdown ml-workflow-demo-kfp-katib-mlflow.ipynb --output README.md`

## Convert Jupyter notebook to code-only notebook

To convert Jupyter notebook to code-only notebook that can be uploaded and executed:
```
jupyter nbconvert --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags="{'text'}" --to notebook ml-workflow-demo-kfp-katib-mlflow.ipynb --output ml-workflow-demo-kfp-katib-mlflow.code.ipynb
```

Code only Jupyter notebook will be created `ml-workflow-demo-kfp-katib-mlflow.code.ipynb`

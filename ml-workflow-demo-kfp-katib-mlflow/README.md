# ML Workflow Demo: Kubeflow - Katib - ML Flow

## Overview

![Diagram](./images/ML-Workflow-Demo-Diagram.png)

## Prerequisites

- Deployed Kubeflow instance and access to Kubeflow dashboard. For sample Kubeflow deployment refer to https://charmed-kubeflow.io/docs/quickstart
- Deployed MLFlow. For deployment of Charmed MLFlow refer to https://charmed-kubeflow.io/docs/mlflow
- Familiarity with Python, Docker, Jupyter notebooks.

## Instructions
The following are the instructions that outline the workflow process.

1. Access Kubeflow dashboard.

2. Navigate to Notebooks.

3. Create a new notebook.
  a. Fill in name
  b. Select Tensorflow image `jupyter-tensorflow-full:v1.6.0`
  c. Select minimum configuration: 4 CPUs and 16GB of RAM

![NotebookCreate](./images/ML-Workflow-NotebookCreate-diag.png)

![NewNotebook](./images/ML-Workflow-NewNotebook-diag.png)

4. Connect to the newly created notebook.

5. Create a Jupyter notebook to hold code that will specify the Kubeflow pipeline.

![NewJupyterNotebook](./images/ML-Workflow-NewJupyterNotebook-diag.png)

NOTE: The following Jupyter notebook contains all the steps outlined below: [ml-workflow-demo-kfp-katib-mlflow,ipynb](./(ml-workflow-demo-kfp-katib-mlflow,ipynb)

6. To setup environment add the following cells to the newly created Jupyter notebook:
```
Setup code goes here
```

7. Create a pipeline step that will do data ingestion and cleanup. Setup transfer of clean data to the next step.
```
Data ingest and cleanup
```

8. Create the next pipeline step that will do hyperparameter tuning using Katib and a training container image docker.io/misohu/kubeflow-training:latest. For more details on the training container image refer to Appendix A of this guide.
```
Katib code
```

9. Create the last step of the pipeline that will do model training using Tensorflow based on Katib tuning results.
```
TF code
```

10. Define a complete pipeline that consists of all steps created earlier.
```
Pipeline code
```

11. Execute pipeline.
```
Pipeline exec code
```

12. Observe run details.

![Run](./images/ML-Workflow-RunDetails.png)

13. Verify that model is stored in MLFlow model registry.

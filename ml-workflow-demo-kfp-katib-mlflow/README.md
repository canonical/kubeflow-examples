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

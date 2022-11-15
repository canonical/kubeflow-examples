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
!pip install kfp==1.8.12
!pip install kubeflow-katib==0.13.0

import json
import kfp
from kfp import dsl
from kfp import Client
from kfp import components
from kfp.onprem import use_k8s_secret
import numpy as np
import pandas as pd
from scipy.io.arff import loadarff
from kubeflow.katib import ApiClient
from kubeflow.katib import V1beta1ExperimentSpec
from kubeflow.katib import V1beta1AlgorithmSpec
from kubeflow.katib import V1beta1ObjectiveSpec
from kubeflow.katib import V1beta1ParameterSpec
from kubeflow.katib import V1beta1FeasibleSpace
from kubeflow.katib import V1beta1TrialTemplate
from kubeflow.katib import V1beta1TrialParameterSpec
```

7. Create a pipeline step that will do data ingestion and cleanup. Setup transfer of clean data to the next step.

```
# Data ingest operation.
# Output is in outputs['data']
ingest_data_op = components.load_component_from_url(
'https://raw.githubusercontent.com/kubeflow/pipelines/master/components/contrib/web/Download/component.yaml'
)
```
```
# Data clean up operation.
def clean_arff_data(
    bucket,
    key,
    input_file: components.InputPath(str)
) -> str:
    import pandas as pd
    import boto3
    import os
    from io import StringIO
    from scipy.io.arff import loadarff

    print(f"Loading input file {input_file}")

    # Convert to dataframe arff format.
    raw_data = loadarff(input_file)
    df_data = pd.DataFrame(raw_data[0].copy())
    print(f"Loaded data file of shape {df_data.shape}")

    # Convert target column to numeric.
    df_data.iloc[:, -1] = pd.get_dummies(df_data['CHURN']).iloc[:, 0]

    # Remove missing values.
    df_clean = df_data.dropna(axis=1)
    df_clean.loc[:,'CHURN']=pd.get_dummies(df_data['CHURN']).iloc[:, 0]

    # Get rid of non-numeric columns.
    df_clean = df_clean.select_dtypes(exclude='object')

    # Save results to S3
    csv_buffer = StringIO()
    df_clean.to_csv(csv_buffer)
    s3_resource = boto3.resource(
        's3',
        endpoint_url='http://minio.kubeflow.svc.cluster.local:9000',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    s3_resouce.create_bucket(bucket)
    print(f"Saving CSV of shape {df_clean.shape} to s3")
    s3_resource.Object(bucket, key).put(Body=csv_buffer.getvalue())

    return "Done"
```

8. Create the next pipeline step that will do hyperparameter tuning using Katib and a training container image docker.io/misohu/kubeflow-training:latest. For more details on the training container image refer to Appendix A of this guide.

```
Katib code
```

9. Create the last step of the pipeline that will do model training using Tensorflow based on Katib tuning results.
```
TF code
```

10. Define a complete pipeline that consists of all steps created earlier. Note that the name of the pipeline must be uqinue. If there was previously defined aq pipeline with the same name and within the same namespace either change the name of current pipeline or delete the older pipeline from the namespace.
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

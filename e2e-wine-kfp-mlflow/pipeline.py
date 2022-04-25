# use virtual env from nb-requirements.txt

import kfp
from kfp import dsl
from kubernetes.client.models import V1EnvVar
from kfp.onprem import use_k8s_secret
from components.preprocess import preprocess
from components.train import train
import os
from pathlib import Path

OUTPUT_DIRECTORY = 'generated'
PROJECT_ROOT = Path(__file__).absolute().parent

web_downloader_op = kfp.components.load_component_from_url(
    'https://raw.githubusercontent.com/kubeflow/pipelines/master/components/contrib/web/Download/component.yaml')

preprocess_op = kfp.components.create_component_from_func(
    func=preprocess,
    output_component_file=os.path.join(PROJECT_ROOT, OUTPUT_DIRECTORY,
                                       'preprocess-component.yaml'),
    # This is optional. It saves the component spec for future use.
    base_image='python:3.9',
    packages_to_install=['pandas', 'pyarrow'])

training_op = kfp.components.create_component_from_func(
    func=train,
    output_component_file=os.path.join(PROJECT_ROOT, OUTPUT_DIRECTORY,
                                       'train-component.yaml'),
    # This is optional. It saves the component spec for future use.
    base_image='python:3.9',
    packages_to_install=['pandas', 'pyarrow', 'sklearn', 'mlflow', 'boto3'])

deploy_op = kfp.components.load_component_from_file(
    os.path.join(PROJECT_ROOT, 'components', 'deploy', 'component.yaml'))


@dsl.pipeline(
    name="e2e_wine_pipeline",
    description="WINE pipeline",
)
def wine_pipeline(url):
    web_downloader_task = web_downloader_op(url=url)
    preprocess_task = preprocess_op(file=web_downloader_task.outputs['data'])

    train_task = (training_op(file=preprocess_task.outputs['output'])
                  .add_env_variable(V1EnvVar(name='MLFLOW_TRACKING_URI',
                                             value='http://mlflow-server.kubeflow.svc.cluster.local:5000'))
                  .add_env_variable(V1EnvVar(name='MLFLOW_S3_ENDPOINT_URL',
                                             value='http://minio.kubeflow.svc.cluster.local:9000'))
                  # https://kubeflow-pipelines.readthedocs.io/en/stable/source/kfp.extensions.html#kfp.onprem.use_k8s_secret
                  .apply(use_k8s_secret(secret_name='mlpipeline-minio-artifact',
                                        k8s_secret_key_to_env={
                                            'accesskey': 'AWS_ACCESS_KEY_ID',
                                            'secretkey': 'AWS_SECRET_ACCESS_KEY',
                                        })))
    deploy_task = deploy_op(model_uri=train_task.output)


if __name__ == '__main__':
    pipeline_output = os.path.join(PROJECT_ROOT, OUTPUT_DIRECTORY,
                                   'wine-pipeline.yaml')
    kfp.compiler.Compiler().compile(wine_pipeline, pipeline_output)
    print('Generated the wine pipeline definition')

# client = kfp.Client()
# client.create_run_from_pipeline_func(
#     wine_pipeline,
#     arguments={
#         "url": "https://raw.githubusercontent.com/Barteus/kubeflow-examples/main/e2e-wine-kfp-mlflow/winequality-red.csv",
#     })

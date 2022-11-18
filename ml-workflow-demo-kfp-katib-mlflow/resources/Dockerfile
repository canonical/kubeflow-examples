FROM docker.io/tensorflow/tensorflow:2.10.0

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./ml-workflow-demo-tf-train-model.py /opt/


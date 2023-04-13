FROM nvcr.io/nvidia/cuda:11.7.1-devel-ubuntu20.04
WORKDIR /app

RUN apt update
RUN apt install python3 python-is-python3 pip -y

RUN pip install --upgrade pip

# Install python packages
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy source code
COPY . .

RUN mkdir -p /root/.cache/torch/hub/checkpoints/
RUN cp ./build/resnet50_a1_0-14fe96d1.pth /root/.cache/torch/hub/checkpoints/resnet50_a1_0-14fe96d1.pth

# Port for GRPC
EXPOSE 5000
# Port for REST
EXPOSE 9000

# Define environment variables
ENV MODEL_NAME ObjectDetection
ENV SERVICE_TYPE MODEL

# Changing folder to default user
RUN chown -R 8888 /app

CMD exec seldon-core-microservice $MODEL_NAME --service-type $SERVICE_TYPE --debug
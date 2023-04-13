# Talking jellyfish demo

The Talking Jellyfish demo is used to showcase using multiple models to solve
the business case.

![](/home/barteus/Work/tutorials/ai-ml-demos/talking-jellyfish/app-diagram.drawio.png)

## Versions

### Version 1.0

Models:

- object detection (detr-resnet-50)
- chatbot (DialoGPT-medium)

Models are created using the hagging face pretrained models, wrapped in
Inference Endpoints and deployed as Seldon Core Deployments.

Models are build locally using the instruction in
the `./models/<model_name>/README.md`. The artifacts are stored in the Docker
repository (local or Dockerhub).

Services:

- Azure speech to text and text to speech

Applications:

- **vision app** - finds humans and notify the chatbot to start the conversation
- **chatbot app** - uses the Azure Speech API to convert sound-to-text and vice
  versa, user inputs are passed into the chatbot endpoint.

Applications are implementing the semaphore pattern using the file (
/tmp/jellyfish-sync.conf). This allows enabling and disabling the communication
for chatbot based on the humans detected in front of it.

## Environment

1. Prepare instance with GPU and install GPUs (check using pytorch or
   tensorflow)
2. Install Microk8s and Kubeflow - https://charmed-kubeflow.io/docs/quickstart
   using the bundle.yaml file.
3. Install python, pip (demo was developed using Python 3.10)

## Models

Build, upload and deploy models based on the `README.md` files for:

- chatbot
- object-detection

Get the model endpoints:

```shell
$ kubectl get svc | grep 8000
chatbot-default                       ClusterIP   10.152.183.11    <none>        8000/TCP,5001/TCP   7d15h
object-detection-default              ClusterIP   10.152.183.182   <none>        8000/TCP,5001/TCP   5d23h
```

Create the environment properties for model urls:

```shell
export CHATBOT_ENDPOINT=http://10.152.183.11:8000/api/v0.1/predictions
export OBJECT_DETECTION_ENDPOINT=http://10.152.183.182:8000/api/v0.1/predictions
```

## Applications

Create the virtual environment using requirements file from `app` folder.

If you want to change the default place of storage for sync config
file (`/tmp/jellyfish-sync.conf`) change it using the environment variable:

```shell
export JELLYFISH_CONFIG_SYNC_FILENAME=/tmp/jellyfish-sync.conf
```

This variable is required for the Windows environments.

In case of application getting stuck remove the config file and restart the
applications.

#### Chatbot

Install Azure CLI:
```shell
sudo apt install curl
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

Create new Azure Speech object and get its key, region.
Set the environment variables:

```shell
export AZURE_SPEECH_KEY=xxx
export AZURE_SPEECH_REGION=xxx
```

Install additional libraries (needed only once):
```shell
sudo apt-get update
sudo apt-get install build-essential libssl-dev libasound2 wget
wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.0g-2ubuntu4_amd64.deb
sudo dpkg -i libssl1.1_1.1.0g-2ubuntu4_amd64.deb
```

Set the model endpoint URL (if you have not done it in the Model section):

```shell
export CHATBOT_ENDPOINT=http://10.152.183.11:8000/api/v0.1/predictions
```

Application by without environment properties uses default microphone and
speaker. This can be changed using environment properties.

```shell
export CHATBOT_USE_DEFAULT_MICROPHONE=False
export CHATBOT_MICROPHONE_DEVICE_NAME=xxx

export CHATBOT_USE_DEFAULT_SPEAKER=False
exprot CHATBOT_SPEAKER_DEVICE_NAME=xxx
```

Run application:

```shell
python chatbot.py
```

#### Vision

First time OpenCV installation requires a bit of additional configuration. You
need libraries when installing it:

```shell
sudo apt install libopencv-dev python3-opencv
```

Export the model endpoint:

```shell
export OBJECT_DETECTION_ENDPOINT=http://10.152.183.182:8000/api/v0.1/predictions
```

The vision application is using the camera with ID 0 and default. You can change
it using environment properties:

```shell
export VISION_USE_CAMERA_ID=0
```

Run application:

```shell
python vision.py
```

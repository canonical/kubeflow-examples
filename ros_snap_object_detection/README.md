# ROS snap object detection

This directory contains a ROS package collecting images from a camera and showing two video stream. One raw and one wiht the inference.

The application is installable as a snap

## How to run
- `docker run --rm --network=host bponieckiklotz/jellyfish.object-detection:dev`
- `sudo snap install ai-kubeflow-demo`
- `sudo snap connect ai-kubeflow-demo:camera`
- `ai-kubeflow-demo server:='localhost'

## How to build
- `sudo snap install snapcraft --classic`
- `snapcraft --enable-experimental-extensions`


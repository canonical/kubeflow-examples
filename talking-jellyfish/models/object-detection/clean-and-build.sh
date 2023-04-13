#!/bin/bash

rm -Rf build
mkdir -p build
wget https://huggingface.co/facebook/detr-resnet-50/resolve/main/config.json -O ./build/config.json
wget https://huggingface.co/facebook/detr-resnet-50/resolve/main/preprocessor_config.json -O ./build/preprocessor_config.json
wget https://huggingface.co/facebook/detr-resnet-50/resolve/main/pytorch_model.bin -O ./build/pytorch_model.bin
wget https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-rsb-weights/resnet50_a1_0-14fe96d1.pth -O ./build/resnet50_a1_0-14fe96d1.pth

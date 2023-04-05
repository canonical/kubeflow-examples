#!/bin/bash

rm -Rf build
mkdir -p build

wget https://huggingface.co/microsoft/DialoGPT-medium/resolve/main/tokenizer_config.json -O ./build/tokenizer_config.json
wget https://huggingface.co/microsoft/DialoGPT-medium/resolve/main/config.json -O ./build/config.json
wget https://huggingface.co/microsoft/DialoGPT-medium/resolve/main/vocab.json -O ./build/vocab.json
wget https://huggingface.co/microsoft/DialoGPT-medium/resolve/main/merges.txt -O ./build/merges.txt
wget https://huggingface.co/microsoft/DialoGPT-medium/resolve/main/pytorch_model.bin -O ./build/pytorch_model.bin
wget https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-rsb-weights/resnet50_a1_0-14fe96d1.pth -O ./build/resnet50_a1_0-14fe96d1.pth

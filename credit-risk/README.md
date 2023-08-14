# Demo for Credit Risk Analysis

Demo overview: <https://excalidraw.com/#json=vg-oXDxr58AcO0GgqXihy,xrH-vQ5Ef5olwQM89CdDZQ>

Dataset: <https://www.kaggle.com/competitions/home-credit-default-risk/data>

## Prerequisite

Create the conda environment.

```bash
conda create -n <env_name>
conda activate <env_name>
```

Install dependencies

### Configure S3 object storage

Create a bucket: bpk-credit-risk-demo

### Configure Kaggle CLI

Configure Kaggle CLI access and set up the API token.
Join the competition: <https://www.kaggle.com/competitions/home-credit-default-risk>

## Setup the data lake

Run script to prepare the data lake:

```bash
bash 01-prep-datalake.sh
```

## Data Scientist notebook

Created based on <https://www.kaggle.com/code/jsaguiar/lightgbm-with-simple-features>

The notebook contains ways to build a model and integrate it with multiple data sources.

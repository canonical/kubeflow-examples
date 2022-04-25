#!/bin/bash

SERVICE_HOSTNAME=$(kubectl get inferenceservice torchserve -n kserve-test -o jsonpath='{.status.url}' | cut -d "/" -f 3)
curl -v -H "Host: ${SERVICE_HOSTNAME}" \
http://${SERVICE_HOSTNAME}/v1/models/mnist:predict \
-d @mnist.json
#!/bin/bash

curl  -s http://10.1.100.61:8000/api/v0.1/predictions \
  -H "Content-Type: application/json" \
  -d '{"data":{"ndarray":[[10.1, 0.37, 0.34, 2.4, 0.085, 5.0, 17.0, 0.99683, 3.17, 0.65, 10.6],[10.1, 0.37, 0.34, 2.4, 0.085, 5.0, 17.0, 0.99683, 3.17, 0.65, 10.6]]}}'

#curl -v "http://10.152.183.130/data-drift/bpk-broker" \
#-X POST \
#-H "Ce-Id: say-hello" \
#-H "Ce-Specversion: 1.0" \
#-H "Ce-Type: greeting" \
#-H "Ce-Source: not-sendoff" \
#-H "Content-Type: application/json" \
#-d '{"msg":"Hello Knative!"}'
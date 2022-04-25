#!/bin/bash

curl  -s http://10.152.183.60:8000/api/v0.1/predictions \
  -H "Content-Type: application/json" \
  -d '{"data":{"ndarray":[[5.6, 0.31, 0.37, 1.4, 0.074, 12.0, 96.0, 0.9954, 3.32, 0.58, 9.2]]}}'
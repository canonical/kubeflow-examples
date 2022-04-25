#!/bin/bash

curl  -s http://10.1.100.27:8000/api/v0.1/predictions \
  -H "Content-Type: application/json" \
  -d '{"data":{"ndarray":[[ 0.4322, -0.5924,  0.5922,  0.7907]]}}'

#!/bin/bash

#CHANGE IP!

#no drift
curl  -s http://10.1.120.156:8000/api/v0.1/predictions \
  -H "Content-Type: application/json" \
  -d '{"data":{"ndarray":[[10.1, 0.37, 0.34, 2.4, 0.085, 5.0, 17.0, 0.99683, 3.17, 0.65, 10.6]]}}'

#drift
curl  -s http://10.1.120.156:8000/api/v0.1/predictions \
  -H "Content-Type: application/json" \
  -d '{"data":{"ndarray":[[8.1, 0.27, 0.41, 1.45, 0.033, 11.0, 63.0, 0.991, 2.99, 0.56, 12.0]]}}'

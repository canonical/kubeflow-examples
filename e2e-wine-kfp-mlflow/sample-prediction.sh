#!/bin/bash

curl  -s http://localhost:8000/api/v0.1/predictions \
  -H "Content-Type: application/json" \
  -d '{"data":{"ndarray":[[10.1, 0.37, 0.34, 2.4, 0.085, 5.0, 17.0, 0.99683, 3.17, 0.65, 10.6],[10.1, 0.37, 0.34, 2.4, 0.085, 5.0, 17.0, 0.99683, 3.17, 0.65, 10.6]]}}'

#curl  -X POST http://10.152.183.174:8000/api/v0.1/feedback \
#  -H "Content-Type: application/json" \
#  -d '{"response": {"data": {"ndarray": [[0.9548873249364059,0.04505474761562512,5.792744796895372e-05]]}}, "truth":{"data": {"ndarray": [[1,0,0]]}}}'

#curl -X POST "http://10.152.183.174:8000/api/v1.0/feedback" \
#        -H "Content-Type: application/json" \
#        -d '{"response": {"data": {"ndarray": [[0.9548873249364059,0.04505474761562512,5.792744796895372e-05]]}}, "truth":{"data": {"ndarray": [[0,0,1]]}}}'
# Object detection

# TODO

- Remove run as root

## Instruction

1. Run `clean-and-build.sh` to download model, weights etc.
2. Build docker image and replace it in deploy.sh

```shell
docker build . -t bponieckiklotz/jellyfish.object-detection:dev
docker push bponieckiklotz/jellyfish.object-detection:dev
```

3. Deploy model using Seldon Core

If you have a single GPU remove the seldon deployment before creating new version. Blue-Green
deployment will not work for you.

```shell
kubectl delete SeldonDeployment object-detection
kubectl apply -f - << END
apiVersion: machinelearning.seldon.io/v1
kind: SeldonDeployment
metadata:
  name: object-detection
spec:
  name: object-detection
  predictors:
  - componentSpecs:
    - spec:
        containers:
        - name: classifier
          image: bponieckiklotz/jellyfish.object-detection:dev@sha256:b19fb9d48e43e1c0a9afe6480553ae506b198d48e347be3f13f9d794f0b5e270
          env:
          - name: HF_DATASETS_OFFLINE
            value: "1"
          - name: TRANSFORMERS_OFFLINE
            value: "1"
          securityContext:
            allowPrivilegeEscalation: false
            runAsUser: 0
          resources:
            limits:
              nvidia.com/gpu: 1
    graph:
      name: classifier
    name: default
    replicas: 1
END
```

## Invoke model

Adjust the model endpoint and image url in the `sample-request.py`. Run
python script. Expected result for default image:

```
Result code 200
{'data': {'names': [], 'ndarray': [{'box': [-0.02, -1.29, 639.61, 374.47], 'label': 'couch', 'score': 0.01456674188375473}, {'box': [0.19, -0.08, 639.36, 387.22], 'label': 'couch', 'score': 0.012890029698610306}, {'box': [40.16, 70.81, 175.55, 117.98], 'label': 'remote', 'score': 0.9982202649116516}, {'box': [17.76, 51.55, 314.45, 366.65], 'label': 'cat', 'score': 0.018895355984568596}, {'box': [333.24, 72.55, 368.33, 187.66], 'label': 'remote', 'score': 0.9960021376609802}, {'box': [-0.02, 1.15, 639.73, 473.76], 'label': 'couch', 'score': 0.9954743981361389}, {'box': [13.24, 52.05, 314.02, 470.93], 'label': 'cat', 'score': 0.99880051612854}, {'box': [-0.14, 1.44, 639.82, 475.24], 'label': 'bed', 'score': 0.07612527906894684}, {'box': [0.36, -1.64, 639.3, 370.48], 'label': 'couch', 'score': 0.011581197381019592}, {'box': [0.03, 96.68, 639.83, 475.06], 'label': 'couch', 'score': 0.011717643588781357}, {'box': [345.4, 23.85, 640.37, 368.72], 'label': 'cat', 'score': 0.9986783862113953}]}, 'meta': {'requestPath': {'classifier': 'localhost:32000/cv:1.0-dev1'}}}
Detected remote with confidence 0.998 at location [40.16, 70.81, 175.55, 117.98]
Detected remote with confidence 0.996 at location [333.24, 72.55, 368.33, 187.66]
Detected couch with confidence 0.995 at location [-0.02, 1.15, 639.73, 473.76]
Detected cat with confidence 0.999 at location [13.24, 52.05, 314.02, 470.93]
Detected cat with confidence 0.999 at location [345.4, 23.85, 640.37, 368.72]

```

## Swagger

Go to the URL of deployed model with suffix `/api/v0.1/doc/`.
If you port-forward to pods directly, then select service/pod with 8000 port
open. 
kubectl apply -f - << END
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: wine-e2e-server
  namespace: admin
spec:
  gateways:
    - kubeflow/kubeflow-gateway
  hosts:
    - '*'
  http:
    - match:
        - uri:
            prefix: /model/wine/
      rewrite:
        uri: /
      route:
        - destination:
            host: mlflow-wine-super-model.admin.svc.cluster.local
            port:
              number: 8000
END

curl -k https://emanager.corp.xperi.com/model/wine/api/v0.1/predictions \
  -H "Content-Type: application/json" \
  -d '{"data":{"ndarray":[[10.1, 0.37, 0.34, 2.4, 0.085, 5.0, 17.0, 0.99683, 3.17, 0.65, 10.6]]}}'\
  -b "authservice_session=<token>"
#{"data":{"names":[],"ndarray":[5.741928028712652]},"meta":{"requestPath":{"classifier":"seldonio/mlflowserver:1.14.0-dev"}}}

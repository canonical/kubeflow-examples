# Knative Eventing+Serving example

1. deploy bundle using juju
2. install knative
3. apply `cloudevents-player.yaml` using kubectl
4. apply `seldon-example.yaml` using kubectl
5. adjust IP and run `simple-call.sh`
6. Check in the cloudevent-player the events.

## Knative Serving hello world

```
kubectl apply hello.yaml -n <namespace>
```
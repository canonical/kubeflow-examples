#
# Setup environment for tests
#
# NOTE: K8S cluster and Juju controller must be installed/deployed prior to running this test.
#
# install tools for testing
sudo snap install jq

# deploy Kubeflow
juju add-model kubeflow
juju deploy kubeflow --trust --channel latest/stable

# deploy COS
juju add-model cos
curl -L https://raw.githubusercontent.com/canonical/cos-lite-bundle/main/overlays/offers-overlay.yaml -O
juju deploy ./cos-lite-bundle.yaml --trust --overlay ./offers-overlay.yaml

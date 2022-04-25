#!/bin/bash

microk8s kubectl create namespace keycloak
microk8s kubectl create -f https://raw.githubusercontent.com/keycloak/keycloak-quickstarts/latest/kubernetes-examples/keycloak.yaml -n keycloak

#create the JSON file

juju config dex-auth static-username="" static-password=""
juju config dex-auth connectors="$(cat oidc-connector.json)"

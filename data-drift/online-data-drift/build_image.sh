#!/bin/bash

VERSION=0.3-dev
REPO=bponieckiklotz/knative-data-drift

docker build . -t $REPO:$VERSION
docker push $REPO:$VERSION

docker inspect --format="{{index .RepoDigests 0}}" "$REPO:$VERSION"
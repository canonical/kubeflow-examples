#!/bin/bash

VERSION=0.1-dev
REPO=bponieckiklotz/tests

sudo docker build . -t $REPO:$VERSION
sudo docker push $REPO:$VERSION

sudo docker inspect --format="{{index .RepoDigests 0}}" "$REPO:$VERSION"
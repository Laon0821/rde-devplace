#!/bin/bash

NAME=sk040
IMAGE_NAME="webserver"
VERSION="1.0.0"

docker build \
  -t ${NAME}-${IMAGE_NAME}:${VERSION} \
  -f Dockerfile .

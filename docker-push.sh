#!/bin/bash

NAME=sk040
IMAGE_NAME="webserver"
VERSION="1.0.0"

DOCKER_REGISTRY="amdp-registry.skala-ai.com/skala25a"
DOCKER_REGISTRY_USER="robot\$skala25a"
DOCKER_REGISTRY_PASSWORD="1qB9cyusbNComZPHAdjNIFWinf52xaBJ"

echo "${DOCKER_REGISTRY_PASSWORD}" | docker login "${DOCKER_REGISTRY}" \
  -u "${DOCKER_REGISTRY_USER}" --password-stdin \
  || { echo "❌ Docker 로그인 실패"; exit 1; }

docker tag "${NAME}-${IMAGE_NAME}:${VERSION}" "${DOCKER_REGISTRY}/${NAME}-${IMAGE_NAME}:${VERSION}"
docker push "${DOCKER_REGISTRY}/${NAME}-${IMAGE_NAME}:${VERSION}" \
  && echo "✅ 이미지 푸시 완료" \
  || echo "❌ 이미지 푸시 실패"

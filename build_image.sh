#!/usr/bin/env bash
source container/.dockerenv

# docker build --no-cache --rm -t ${IMAGE_NAME} .
DOCKER_BUILDKIT=0 docker build --rm -t ${IMAGE_NAME} . -f container/Dockerfile --build-arg MODEL=${MODEL}


#!/bin/bash
set -ex
mypy .
./manage.py collectstatic --no-input
docker buildx build --platform=linux/amd64,linux/arm64 -t holdenk/pcfweb:v0.2.0c . --push


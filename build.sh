#!/bin/bash
set -ex
docker buildx build --platform=linux/amd64,linux/arm64 -t holdenk/pcfweb:v0.0.1 . --push


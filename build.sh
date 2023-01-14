#!/bin/bash
set -ex
mypy -p main -p pigscanfly
./manage.py collectstatic --no-input
# Hack, for now.
rm -rf ./cal-sync-magic
cp -af ../cal-sync-magic ./
docker buildx build --platform=linux/amd64,linux/arm64 -t holdenk/pcfweb:v0.4.1c . --push


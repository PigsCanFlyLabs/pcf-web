#!/bin/bash
set -ex
mypy .
./manage.py collectstatic --no-input
# Hack, for now.
cp -af ../cal-sync-magic/cal_sync_magic ./
docker buildx build --platform=linux/amd64,linux/arm64 -t holdenk/pcfweb:v0.3.0b . --push


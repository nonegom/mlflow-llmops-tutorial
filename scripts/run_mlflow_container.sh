#!/usr/bin/env bash

IMAGE="${1:-ghcr.io/mlflow/mlflow:v3.3.0}"
HOST_DIR="$(pwd)"
CONTAINER_NAME="${CONTAINER_NAME:-mlflow-server}"
HOST_PORT="${HOST_PORT:-5000}"
CONTAINER_PORT="${CONTAINER_PORT:-5000}"
VOLUME_DIR_NAME="${VOLUME_DIR_NAME:-mlflow}"
VOLUME_PATH="$HOST_DIR/$VOLUME_DIR_NAME"
HOST_IP="${HOST_IP:-0.0.0.0}"

MSYS_NO_PATHCONV=1 docker run -it \
  --name "$CONTAINER_NAME" \
  -p "$HOST_PORT:$CONTAINER_PORT" \
  -v "$VOLUME_PATH:/mlruns" \
  "$IMAGE" \
  mlflow server \
  --host "$HOST_IP" \
  --backend-store-uri /mlruns \
  --default-artifact-root /mlruns

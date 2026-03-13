#!/usr/bin/env bash
set -euo pipefail

SERVER_USER=${SERVER_USER:-hadoop}
SERVER_HOST=${SERVER_HOST:-server-node}
SERVER_DIR=${SERVER_DIR:-~/incoming_logs}
LOCAL_DIR=${LOCAL_DIR:-./logs}

if [ ! -d "$LOCAL_DIR" ]; then
  echo "Local log dir not found: $LOCAL_DIR" >&2
  exit 1
fi

ssh "$SERVER_USER@$SERVER_HOST" "mkdir -p $SERVER_DIR"
scp "$LOCAL_DIR"/*.log "$SERVER_USER@$SERVER_HOST:$SERVER_DIR/"

echo "Transferred logs to $SERVER_USER@$SERVER_HOST:$SERVER_DIR"

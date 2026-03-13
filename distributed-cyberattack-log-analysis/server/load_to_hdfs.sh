#!/usr/bin/env bash
set -euo pipefail

IN_DIR=${IN_DIR:-~/incoming_logs}
HDFS_WEB_DIR=${HDFS_WEB_DIR:-/logs/web}
HDFS_AUTH_DIR=${HDFS_AUTH_DIR:-/logs/auth}
HDFS_SYSTEM_DIR=${HDFS_SYSTEM_DIR:-/logs/system}

hdfs dfs -mkdir -p "$HDFS_WEB_DIR" "$HDFS_AUTH_DIR" "$HDFS_SYSTEM_DIR"

if [ -f "$IN_DIR/web.log" ]; then
  hdfs dfs -put -f "$IN_DIR"/web.log "$HDFS_WEB_DIR"/
fi
if [ -f "$IN_DIR/auth.log" ]; then
  hdfs dfs -put -f "$IN_DIR"/auth.log "$HDFS_AUTH_DIR"/
fi
if [ -f "$IN_DIR/system.log" ]; then
  hdfs dfs -put -f "$IN_DIR"/system.log "$HDFS_SYSTEM_DIR"/
fi

echo "Loaded logs to HDFS"

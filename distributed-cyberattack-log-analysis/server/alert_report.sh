#!/usr/bin/env bash
set -euo pipefail

OUT_DIR=${OUT_DIR:-./reports}
mkdir -p "$OUT_DIR"
TS=$(date +%Y%m%d_%H%M%S)

TSV_PATH="$OUT_DIR/alerts_$TS.tsv"
CSV_PATH="$OUT_DIR/alerts_$TS.csv"
LATEST_TSV="$OUT_DIR/alerts_latest.tsv"

hdfs dfs -test -e /alerts/auth && AUTH_SRC="/alerts/auth/part-*"
hdfs dfs -test -e /alerts/web && WEB_SRC="/alerts/web/part-*"

if [ -z "${AUTH_SRC:-}" ] && [ -z "${WEB_SRC:-}" ]; then
  echo "No alert outputs found in HDFS." >&2
  exit 1
fi

hdfs dfs -cat ${AUTH_SRC:-} ${WEB_SRC:-} > "$TSV_PATH"
cp "$TSV_PATH" "$LATEST_TSV"

# Convert to CSV with header
{
  echo "attack_type,ip,count,first_timestamp,last_timestamp"
  awk -F'\t' 'BEGIN{OFS=","} {print $2,$3,$4,$5,$6}' "$TSV_PATH"
} > "$CSV_PATH"

echo "Report saved to:"
echo "  $TSV_PATH"
echo "  $CSV_PATH"

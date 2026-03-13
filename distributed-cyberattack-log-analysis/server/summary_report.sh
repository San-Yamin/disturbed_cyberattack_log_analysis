#!/usr/bin/env bash
set -euo pipefail

OUT_DIR=${OUT_DIR:-./reports}
ALERTS_TSV=${ALERTS_TSV:-$OUT_DIR/alerts_latest.tsv}
mkdir -p "$OUT_DIR"

if [ ! -f "$ALERTS_TSV" ]; then
  echo "alerts_latest.tsv not found. Run alert_report.sh first." >&2
  exit 1
fi

count_hdfs_lines() {
  local pattern=$1
  local count
  count=$(hdfs dfs -cat $pattern 2>/dev/null | wc -l | tr -d ' ') || count=0
  echo "${count:-0}"
}

TOTAL_WEB=$(count_hdfs_lines "/logs/web/*")
TOTAL_AUTH=$(count_hdfs_lines "/logs/auth/*")
TOTAL_SYSTEM=$(count_hdfs_lines "/logs/system/*")
TOTAL_LOGS=$((TOTAL_WEB + TOTAL_AUTH + TOTAL_SYSTEM))

TOTAL_ALERT_RECORDS=$(awk 'END{print NR+0}' "$ALERTS_TSV")
TOTAL_ATTACK_EVENTS=$(awk -F'\t' '{sum+=$4} END{print sum+0}' "$ALERTS_TSV")

ATTACK_COUNTS="$OUT_DIR/attack_counts.tsv"
TOP_IPS="$OUT_DIR/top_ips.tsv"
TEMPORAL="$OUT_DIR/temporal_distribution.tsv"
SUMMARY_TXT="$OUT_DIR/summary_report.txt"
SUMMARY_JSON="$OUT_DIR/summary_report.json"

awk -F'\t' '{count[$2]+=$4} END{for (t in count) print t, count[t]}' "$ALERTS_TSV" \
  | sort -k2,2nr > "$ATTACK_COUNTS"

awk -F'\t' '{ip[$3]+=$4} END{for (i in ip) print i, ip[i]}' "$ALERTS_TSV" \
  | sort -k2,2nr | head -10 > "$TOP_IPS"

awk -F'\t' '{
  split($5, dt, " ");
  if (length(dt[2])>=2) {hour=substr(dt[2],1,2)} else {hour="00"}
  key=dt[1]" "hour":00";
  bucket[key]+=$4
} END{for (k in bucket) print k, bucket[k]}' "$ALERTS_TSV" \
  | sort > "$TEMPORAL"

cat > "$SUMMARY_TXT" <<EOF
Summary Statistics Report
-------------------------
Total logs processed: $TOTAL_LOGS (web=$TOTAL_WEB, auth=$TOTAL_AUTH, system=$TOTAL_SYSTEM)
Total alert records: $TOTAL_ALERT_RECORDS
Total attack events (sum of counts): $TOTAL_ATTACK_EVENTS

Attack counts per category: $ATTACK_COUNTS
Top attacker IPs: $TOP_IPS
Temporal distribution (by hour): $TEMPORAL
EOF

cat > "$SUMMARY_JSON" <<EOF
{
  "total_logs_processed": $TOTAL_LOGS,
  "total_web_logs": $TOTAL_WEB,
  "total_auth_logs": $TOTAL_AUTH,
  "total_system_logs": $TOTAL_SYSTEM,
  "total_alert_records": $TOTAL_ALERT_RECORDS,
  "total_attack_events": $TOTAL_ATTACK_EVENTS,
  "attack_counts_tsv": "$(basename "$ATTACK_COUNTS")",
  "top_ips_tsv": "$(basename "$TOP_IPS")",
  "temporal_distribution_tsv": "$(basename "$TEMPORAL")"
}
EOF

echo "Summary reports saved to:"
echo "  $SUMMARY_TXT"
echo "  $SUMMARY_JSON"
echo "  $ATTACK_COUNTS"
echo "  $TOP_IPS"
echo "  $TEMPORAL"

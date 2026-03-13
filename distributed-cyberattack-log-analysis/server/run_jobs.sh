#!/usr/bin/env bash
set -euo pipefail

HADOOP_HOME=${HADOOP_HOME:-/usr/local/hadoop}
STREAMING_JAR=${HADOOP_STREAMING_JAR:-$(ls "$HADOOP_HOME"/share/hadoop/tools/lib/hadoop-streaming-*.jar | head -n 1)}

if [ ! -f "$STREAMING_JAR" ]; then
  echo "Streaming jar not found. Set HADOOP_STREAMING_JAR." >&2
  exit 1
fi

# Thresholds (override via env)
export BRUTE_THRESHOLD=${BRUTE_THRESHOLD:-5}
export DDOS_THRESHOLD=${DDOS_THRESHOLD:-100}
export SQLI_THRESHOLD=${SQLI_THRESHOLD:-1}
export XSS_THRESHOLD=${XSS_THRESHOLD:-1}

# Clean old outputs
hdfs dfs -rm -r -f /alerts/auth /alerts/web || true

# Brute-force detection
hadoop jar "$STREAMING_JAR" \
  -cmdenv BRUTE_THRESHOLD="$BRUTE_THRESHOLD" \
  -input /logs/auth/ \
  -output /alerts/auth/ \
  -mapper "python3 mapper_auth.py" \
  -reducer "python3 reducer_auth.py" \
  -file mapper_auth.py -file reducer_auth.py

# Web attacks + DDoS
hadoop jar "$STREAMING_JAR" \
  -cmdenv DDOS_THRESHOLD="$DDOS_THRESHOLD" \
  -cmdenv SQLI_THRESHOLD="$SQLI_THRESHOLD" \
  -cmdenv XSS_THRESHOLD="$XSS_THRESHOLD" \
  -input /logs/web/ \
  -output /alerts/web/ \
  -mapper "python3 mapper_web.py" \
  -reducer "python3 reducer_web.py" \
  -file mapper_web.py -file reducer_web.py

echo "MapReduce jobs complete"

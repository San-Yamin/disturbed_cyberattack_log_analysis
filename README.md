# Distributed Cyberattack Log Analysis System using Hadoop

This project demonstrates a **distributed client–server log analysis pipeline** using **Hadoop, HDFS, and MapReduce (via Hadoop Streaming in Python)** to detect cyberattacks using **rule-based detection**.

## Architecture (Minimum Distributed Setup)
- **Client node**: generates realistic web + auth logs and transfers them to server
- **Server node**: Hadoop NameNode + DataNode; HDFS storage; MapReduce analysis

Scalability is achieved by adding more client nodes and DataNodes.
Fault tolerance is handled by HDFS replication.

## Folder Structure
```
client/
  log_generator.py
  send_logs.sh
server/
  load_to_hdfs.sh
  mapper_auth.py
  reducer_auth.py
  mapper_web.py
  reducer_web.py
  run_jobs.sh
  alert_report.sh
  summary_report.sh
dashboard/
  app.py (optional UI)
  requirements.txt
```

## Requirements
- Linux/macOS/Windows (with WSL or Git Bash)
- Hadoop 3.3.x (recommended) installed on server node
- Python 3.x on both client and server nodes

## Quick Start (Demo)
### 1) Client: Generate logs
```
cd client
python3 log_generator.py --out-dir ./logs --web-lines 5000 --auth-lines 1500 --system-lines 800
```

### 2) Client: Transfer logs to server
```
export SERVER_USER=hadoop
export SERVER_HOST=server-node
export SERVER_DIR=~/incoming_logs
./send_logs.sh
```
For periodic transfer, schedule `send_logs.sh` with `cron` on the client.

### 3) Server: Load into HDFS
```
cd server
export IN_DIR=~/incoming_logs
./load_to_hdfs.sh
```

### 4) Server: Run MapReduce detection
```
./run_jobs.sh
```

### 5) Server: Export alerts
```
./alert_report.sh
```

### 6) Server: Summary statistics (optional)
```
./summary_report.sh
```

## Detection Rules
- **Brute-force**: >= 5 failed logins per IP per minute
- **DDoS**: >= 100 requests per IP per minute
- **SQL Injection**: suspicious SQL patterns in URL
- **XSS**: script injection patterns in URL

Thresholds can be adjusted via env vars:
```
BRUTE_THRESHOLD=5 DDOS_THRESHOLD=100 SQLI_THRESHOLD=1 XSS_THRESHOLD=1
```

## Output Format
Each alert is printed as TSV (HDFS output):
```
ALERT  TYPE  IP  COUNT  FIRST_TS  LAST_TS
```

Exported local reports:
- `alerts_YYYYMMDD_HHMMSS.tsv`
- `alerts_YYYYMMDD_HHMMSS.csv`
- `alerts_latest.tsv`
- `summary_report.txt` and `summary_report.json`

## Notes
- This system uses **rule-based detection only** (no ML/AI).
- For university demos, this is ideal because the pipeline is clear and reproducible.

## Documentation
- Final report: `docs/final_report.md`
- Presentation: `docs/presentation.pptx` (backup: `docs/presentation.md`)

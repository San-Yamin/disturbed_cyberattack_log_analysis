---
title: Distributed Cyberattack Log Analysis System using Hadoop
subtitle: Final-Year Distributed Systems Project
---

# Problem Statement
- Massive logs require distributed storage + processing
- Detect common attacks using rule-based methods
- Use Hadoop, HDFS, MapReduce with Python Streaming

# Architecture (Minimum Distributed Setup)
- Client node: log generation + transfer
- Server node: NameNode + DataNode + MapReduce
- HDFS stores logs, MR analyzes in parallel

# Log Sources
- Web server access logs (HTTP requests)
- System auth logs (SSH failures)
- System logs (service/kernel events)

# Data Flow Pipeline
1. Client generates logs
2. Transfer to server
3. Store in HDFS
4. MapReduce detection
5. Alerts + reports

# Attack Types Detected
- Brute-force login (auth logs)
- SQL Injection (web logs)
- XSS (web logs)
- DDoS (web logs)

# Rule-Based Logic
- Brute-force: >=5 fails/IP/min
- DDoS: >=100 req/IP/min
- SQLi/XSS: pattern match in URL

# Technologies
- Hadoop 3.3.x, HDFS, MapReduce
- Hadoop Streaming with Python
- Bash automation
- Linux VMs (client + server)

# Demo Steps
1. Generate logs (client)
2. Transfer logs (scp)
3. Load into HDFS
4. Run MR jobs
5. View alerts

# Output Example
ALERT  TYPE  IP  COUNT  FIRST_TS  LAST_TS
ALERT  DDOS  10.1.1.7  145  2026-02-04 13:12:01  2026-02-04 13:12:59

# Reports (Outputs)
- Attack Detection Report (HDFS + CSV/TSV)
- Summary Statistics Report
- Optional Dashboard (Flask)

# Scalability + Fault Tolerance
- Add more clients or DataNodes
- HDFS replication protects data
- MapReduce runs in parallel

# Conclusion
- Clear distributed pipeline
- Reproducible detection
- Suitable for large-scale logs

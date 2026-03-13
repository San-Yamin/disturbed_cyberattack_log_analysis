# Distributed Cyberattack Log Analysis System using Hadoop

## 1. Abstract
This project designs and implements a distributed cyber‑security log analysis system using Apache Hadoop. The system follows a client–server architecture where a client node generates realistic authentication and web server logs and transfers them to a Hadoop server. Logs are stored in HDFS for fault‑tolerant, scalable storage and analyzed in parallel using MapReduce through Hadoop Streaming with Python. The system detects brute‑force logins, SQL Injection, Cross‑Site Scripting (XSS), and DDoS attacks using deterministic rule‑based detection (no ML/AI). The project demonstrates core distributed systems concepts—distribution, parallelism, fault tolerance, scalability, and data locality—while remaining realistic for a university laboratory environment.

## 2. Introduction and Background Study
Modern systems generate large volumes of logs from web servers, authentication services, and system processes. Analyzing these logs on a single machine becomes slow and unreliable as data grows. Distributed systems solve this problem by distributing data and computation across multiple nodes. Hadoop is a widely used framework for this purpose: HDFS stores data in a distributed, replicated form, and MapReduce provides parallel processing. For cyber‑security, logs are essential evidence for detecting attacks such as brute‑force attempts or injection attacks. This project builds a small‑scale but realistic system that uses Hadoop to analyze security logs at scale.

## 3. Detailed Problem Statement
Universities and organizations require scalable systems to detect cyberattacks from massive logs. Traditional centralized log analysis does not scale and suffers from single points of failure. The problem is to design a distributed system that:
- Ingests large volumes of logs from client nodes,
- Stores them reliably and scalably,
- Processes them in parallel,
- Detects known cyberattack patterns using rule‑based methods,
- Produces clear reports suitable for academic evaluation.

## 4. Motivation and Significance
- Log data is large and continuously generated.
- Security teams need quick, reliable detection of common attacks.
- Distributed systems provide scalability and fault tolerance.
This project bridges distributed systems theory with practical cyber‑security analysis in a student‑implementable way.

## 5. Project Objectives (Technical + Academic)
**Technical objectives**
- Implement a client–server architecture for log generation, transfer, and storage.
- Use HDFS for fault‑tolerant distributed storage.
- Use Hadoop Streaming with Python for MapReduce analysis.
- Detect brute‑force, SQLi, XSS, and DDoS attacks using rules.

**Academic objectives**
- Demonstrate distributed systems concepts in a concrete project.
- Provide a structured report and presentation for final‑year evaluation.
- Produce reproducible outputs for viva defense.

## 6. Scope of the Project and Assumptions
**Scope**
- One client node and one Hadoop server node (pseudo‑distributed cluster).
- Log analysis at lab scale (thousands to millions of lines).
- Rule‑based detection only.

**Assumptions**
- Hadoop 3.3.x is available on the server node.
- Logs follow Apache/Nginx and Linux auth.log formats.
- Time windows are minute‑level for brute‑force and DDoS detection.

## 7. Literature Review (Brief)
- **Log analysis:** Common practice in security monitoring and incident response.
- **Hadoop and HDFS:** Standard distributed storage for large datasets.
- **MapReduce:** Parallel model for large‑scale data processing.
- **Rule‑based cyber‑attack detection:** Reliable for known patterns (e.g., SQLi/XSS), with low computational overhead.

## 8. Overall System Architecture
### 8.1 Logical Architecture
- **Client Layer:** Generates logs and transfers them to the server.
- **Storage Layer:** HDFS stores logs with replication for fault tolerance.
- **Processing Layer:** MapReduce jobs analyze logs in parallel.
- **Reporting Layer:** Outputs alerts and summary statistics.

### 8.2 Physical Architecture (Minimum Setup)
- **Client VM:** Log generator + transfer script.
- **Server VM:** Hadoop NameNode + DataNode (single host, pseudo‑distributed).

**Scalability path:** Multiple client nodes can send logs, and multiple DataNodes can be added to the server side for higher storage and compute capacity.

## 9. Distributed Systems Concepts Applied
- **Distribution:** Logs are generated remotely and stored across HDFS blocks.
- **Parallelism:** MapReduce processes different blocks in parallel.
- **Fault tolerance:** HDFS replication protects against node failure.
- **Scalability:** Adding nodes increases storage/compute linearly.
- **Data locality:** MapReduce runs tasks near data blocks to reduce network load.

## 10. Detailed Data Flow and Processing Workflow
1. Client generates auth, system, and web logs.
2. Client transfers logs to server via SCP/RSYNC.
3. Server loads logs into HDFS `/logs/auth`, `/logs/web`, and `/logs/system`.
4. MapReduce runs:
   - Auth job → brute‑force detection.
   - Web job → SQLi/XSS/DDoS detection.
5. Output written to HDFS `/alerts/auth` and `/alerts/web`.
6. Exported report generated locally on server.

## 11. Hadoop Ecosystem Components and Justification
- **HDFS:** Distributed, fault‑tolerant storage for large log files.
- **MapReduce:** Batch‑oriented distributed processing suitable for log scanning.
- **Hadoop Streaming:** Enables Python mappers/reducers for rapid development.

## 12. HDFS Directory Structure and Data Organization
```
/logs/auth/    -> authentication logs
/logs/web/     -> web access logs
/logs/system/  -> system logs
/alerts/auth/  -> brute‑force alerts
/alerts/web/   -> SQLi/XSS/DDoS alerts
```
This separation improves clarity, access control, and workflow management.

## 13. MapReduce Workflow using Hadoop Streaming (Python)
- **Mapper:** Parse each log line, emit `(key, timestamp)` pairs.
- **Reducer:** Aggregate counts per key, track min/max timestamps, apply thresholds, emit alerts.
Streaming allows Python to be used directly without Java.

## 14. Rule‑Based Attack Detection Methodology
**Brute‑Force**
- Rule: `failed_logins(IP, minute) >= 5`

**DDoS**
- Rule: `requests(IP, minute) >= 100`

**SQL Injection**
- Rule: URI contains SQLi patterns such as `UNION SELECT`, `' OR '1'='1'`, `--`, `DROP`.

**XSS**
- Rule: URI contains `<script>`, `onerror=`, `alert(`.

Thresholds are configurable via environment variables.

## 15. Programming Languages and Tools Used (Justification)
- **Python:** Fast development for log generation and streaming MR logic.
- **Bash:** Automates transfers, HDFS loading, and job execution.
- **VS Code:** Lightweight IDE for cross‑platform demonstration.
- **Hadoop 3.3.x:** Stable academic version with full HDFS + MR support.

## 16. Implementation Details (Student‑Realistic)
- Single server VM runs NameNode + DataNode in pseudo‑distributed mode.
- Client VM produces logs locally (Python script).
- Scripts automate end‑to‑end flow with clear commands.
- Periodic transfer can be scheduled using `cron` (e.g., every 10 minutes).
- All outputs are text‑based for easy review and grading.

## 17. Input Log Format Examples and Dataset Description
**Web log (Apache/Nginx style)**
```
10.0.0.5 - - [04/Feb/2026:13:12:22 +0000] "GET /search?q=test HTTP/1.1" 200 512 "-" "Mozilla/5.0"
```
**Auth log (Linux sshd)**
```
Feb 04 13:12:22 client-node sshd[1234]: Failed password for invalid user bob from 10.0.0.7 port 22
```
**System log (syslog style)**
```
Feb 04 13:12:22 client-node systemd[1]: Started Daily Cleanup Service.
```

**Dataset description**
- Generated using the provided Python log generator.
- Includes normal traffic plus injected attack patterns.
- Scale can be configured (e.g., 5,000 web lines and 1,500 auth lines).

## 18. Output Format and Security Analysis Report
**Primary report (mandatory)**
- Stored in HDFS and exported locally as TSV/CSV.
```
ALERT  TYPE  IP  COUNT  FIRST_TS  LAST_TS
```
**Output options supported**
1. **Attack Detection Report** (mandatory) — HDFS text + exported CSV/TSV.
2. **Summary Statistics Report** — totals, category counts, top IPs, temporal distribution.
3. **Optional Dashboard** — Flask UI that reads the exported TSV.

## 19. Performance, Scalability, and Fault‑Tolerance Discussion
- **Performance:** MapReduce scans logs in parallel; time reduces as nodes increase.
- **Scalability:** New DataNodes add storage and compute capacity; new clients add data sources.
- **Fault tolerance:** HDFS replication preserves data if nodes fail; MR can re‑run failed tasks.
- **Data locality:** Tasks run on nodes that host blocks, reducing network overhead.

## 20. Advantages of the Proposed System
- Clear distributed workflow aligned with theory.
- Deterministic, explainable detection rules.
- Low resource requirements for lab‑scale demos.
- Easy to extend with new attacks or additional logs.

## 21. Limitations and Constraints
- Rule‑based detection does not catch unknown attacks.
- Accuracy depends on log format consistency.
- Single‑server pseudo‑distributed cluster does not fully mimic production scale.

## 22. Security, Privacy, and Ethical Considerations
- Logs can contain sensitive data; access should be restricted.
- Use synthetic data for academic demos.
- Reports should avoid exposing real user information.

## 23. Future Enhancements and Extensibility
- Add more log sources (firewall, DNS, IDS).
- Implement multi‑stage MapReduce for session tracking.
- Add anomaly detection (optional ML module).
- Integrate a real‑time layer (Kafka + Spark Streaming).

## 24. Conclusion
The proposed system demonstrates a realistic distributed security analytics pipeline using Hadoop. It shows how HDFS and MapReduce provide scalable, fault‑tolerant processing for large log data. The project is academically strong, technically feasible, and suitable for final‑year demonstration and viva defense.

## 25. Presentation‑Ready Summary (10–15 Minutes)
1. Problem: Large logs require distributed analysis for cyber‑security.
2. Solution: Hadoop‑based client–server system with HDFS + MapReduce.
3. Architecture: Client generates logs; server stores and processes in parallel.
4. Detection: Brute‑force, SQLi, XSS, DDoS using rule‑based thresholds.
5. Results: Alerts and summary statistics exported for reporting.
6. Distributed systems concepts: scalability, fault tolerance, data locality.
7. Conclusion: Clear academic demonstration with practical relevance.

## 26. Viva / Defense Questions with Strong Answers
**Q1: Why use Hadoop instead of a single machine?**  
A: Hadoop distributes storage and compute; it scales with data size and provides fault tolerance through HDFS replication.

**Q2: How does MapReduce provide parallelism?**  
A: Input logs are split into blocks; mappers process blocks independently, reducers aggregate results across blocks.

**Q3: What is data locality?**  
A: Hadoop schedules tasks on nodes that contain the data blocks, reducing network transfer.

**Q4: Why rule‑based detection only?**  
A: Rule‑based detection is explainable, deterministic, and suitable for final‑year demonstration without ML complexity.

**Q5: How does HDFS handle failures?**  
A: Data blocks are replicated across multiple nodes; if one fails, another copy remains accessible.

**Q6: How can this system scale to multiple clients?**  
A: Each client can generate and transfer logs to the server; HDFS and MapReduce can process the combined dataset.

**Q7: How can accuracy be improved?**  
A: By refining detection rules, adding context (sessions), or incorporating optional anomaly detection in future work.

**Q8: What are the main limitations?**  
A: Rule‑based detection misses unknown attacks and depends on consistent log formats.

**Q9: What is the benefit of Hadoop Streaming?**  
A: It allows the use of Python for mappers/reducers without Java, enabling faster development.

**Q10: How do you verify results?**  
A: Attack patterns are injected during log generation, and alerts confirm they are detected with expected counts.

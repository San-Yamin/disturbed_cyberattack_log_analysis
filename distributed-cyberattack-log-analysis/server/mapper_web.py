#!/usr/bin/env python3
import re, sys
from datetime import datetime
from urllib.parse import unquote

# Common log format parser
PAT = re.compile(r'^(?P<ip>\d+\.\d+\.\d+\.\d+)\s+-\s+-\s+\[(?P<ts>[^\]]+)\]\s+"(?P<method>\w+)\s+(?P<path>[^\s]+)')

SQLI = ["' or '1'='1", "union select", "--", "; drop", "%27%20or%201%3d1"]
XSS = ["<script", "%3cscript%3e", "onerror=", "alert("]

for line in sys.stdin:
    m = PAT.search(line)
    if not m:
        continue
    ip = m.group('ip')
    ts_raw = m.group('ts')  # dd/Mon/YYYY:HH:MM:SS +/-ZZZZ
    raw_path = m.group('path')
    path = unquote(raw_path).lower()

    try:
        dt = datetime.strptime(ts_raw, "%d/%b/%Y:%H:%M:%S %z")
        ts = dt.strftime("%Y-%m-%d %H:%M:%S")
        window = dt.strftime("%Y-%m-%d %H:%M")
    except ValueError:
        # Fallback: keep raw timestamp if parsing fails
        ts = ts_raw
        window = ts_raw.split(':')[0] + ':' + ts_raw.split(':')[1]

    # DDoS: count every request per IP per minute
    print(f"DDOS|{ip}|{window}\t{ts}")

    # SQLi
    if any(pat in path for pat in SQLI):
        print(f"SQLI|{ip}\t{ts}")

    # XSS
    if any(pat in path for pat in XSS):
        print(f"XSS|{ip}\t{ts}")

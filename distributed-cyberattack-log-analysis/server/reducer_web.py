#!/usr/bin/env python3
import sys, os

sqli_threshold = int(os.environ.get('SQLI_THRESHOLD', '1'))
xss_threshold = int(os.environ.get('XSS_THRESHOLD', '1'))
ddos_threshold = int(os.environ.get('DDOS_THRESHOLD', '100'))

current = None
count = 0
min_ts = None
max_ts = None

thresholds = {
    'SQLI': sqli_threshold,
    'XSS': xss_threshold,
    'DDOS': ddos_threshold,
}

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    key, ts = line.split('\t', 1)
    if key != current:
        if current is not None:
            parts = current.split('|')
            kind = parts[0]
            ip = parts[1]
            if count >= thresholds[kind]:
                label = {'SQLI':'SQL_INJECTION','XSS':'XSS','DDOS':'DDOS'}[kind]
                print(f"ALERT\t{label}\t{ip}\t{count}\t{min_ts}\t{max_ts}")
        current = key
        count = 0
        min_ts = None
        max_ts = None
    count += 1
    if min_ts is None or ts < min_ts:
        min_ts = ts
    if max_ts is None or ts > max_ts:
        max_ts = ts

if current is not None:
    parts = current.split('|')
    kind = parts[0]
    ip = parts[1]
    if count >= thresholds[kind]:
        label = {'SQLI':'SQL_INJECTION','XSS':'XSS','DDOS':'DDOS'}[kind]
        print(f"ALERT\t{label}\t{ip}\t{count}\t{min_ts}\t{max_ts}")

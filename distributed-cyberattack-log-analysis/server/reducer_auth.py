#!/usr/bin/env python3
import sys, os

threshold = int(os.environ.get('BRUTE_THRESHOLD', '5'))

current = None
count = 0
min_ts = None
max_ts = None

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    key, ts = line.split('\t', 1)
    if key != current:
        if current is not None and count >= threshold:
            kind, ip, _window = current.split('|')
            print(f"ALERT\tBRUTE_FORCE\t{ip}\t{count}\t{min_ts}\t{max_ts}")
        current = key
        count = 0
        min_ts = None
        max_ts = None
    count += 1
    if min_ts is None or ts < min_ts:
        min_ts = ts
    if max_ts is None or ts > max_ts:
        max_ts = ts

if current is not None and count >= threshold:
    kind, ip, _window = current.split('|')
    print(f"ALERT\tBRUTE_FORCE\t{ip}\t{count}\t{min_ts}\t{max_ts}")

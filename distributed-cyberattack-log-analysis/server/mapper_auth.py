#!/usr/bin/env python3
import re, sys
from datetime import datetime

# Example: Feb 04 13:12:22 host sshd[1234]: Failed password for invalid user bob from 10.0.0.1 port 22
PAT = re.compile(r'^(?P<mon>\w{3})\s+(?P<day>\d{1,2})\s+(?P<time>\d{2}:\d{2}:\d{2}).*Failed password.*from (?P<ip>\d+\.\d+\.\d+\.\d+)')

MONTHS = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}

current_year = datetime.now().year

for line in sys.stdin:
    m = PAT.search(line)
    if not m:
        continue
    mon = MONTHS[m.group('mon')]
    day = int(m.group('day'))
    t = m.group('time')
    ip = m.group('ip')

    # Timestamp format for ordering: YYYY-MM-DD HH:MM:SS
    ts = f"{current_year:04d}-{mon:02d}-{day:02d} {t}"
    window = f"{current_year:04d}-{mon:02d}-{day:02d} {t[:5]}"
    print(f"BRUTE|{ip}|{window}\t{ts}")

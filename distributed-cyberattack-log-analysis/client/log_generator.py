#!/usr/bin/env python3
"""
Generate realistic web and auth logs with injected attack patterns.
"""
import argparse
import random
import time
from datetime import datetime, timedelta
from pathlib import Path

WEB_PATHS = [
    "/", "/index.html", "/login", "/signup", "/search?q=distributed+systems",
    "/products", "/products?id=10", "/cart", "/api/v1/items", "/admin"
]
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "curl/7.79.1"
]
STATUS_CODES = [200, 200, 200, 302, 404, 500]
METHODS = ["GET", "POST"]
USERS = ["alice", "bob", "charlie", "dave", "eve", "mallory", "admin"]
SYSTEM_MESSAGES = [
    "kernel: [UFW BLOCK] IN=eth0 OUT= MAC=.. SRC={ip} DST=10.0.0.2 PROTO=TCP SPT=443 DPT=22",
    "cron[1234]: (root) CMD (/usr/lib/sa/sa1 1 1)",
    "systemd[1]: Started Daily Cleanup Service.",
    "sudo: user : TTY=pts/0 ; PWD=/home/user ; USER=root ; COMMAND=/usr/bin/apt update",
    "sshd[2345]: Received disconnect from {ip}: 11: Bye Bye",
    "nginx[777]: signal process started",
    "docker[888]: container {cid} started"
]

SQLI_PATTERNS = [
    "' OR '1'='1", "UNION SELECT", "--", "; DROP TABLE users;", "%27%20OR%201%3D1"
]
XSS_PATTERNS = [
    "<script>alert(1)</script>", "%3Cscript%3Ealert(1)%3C%2Fscript%3E", "onerror=alert(1)", "alert(1)"
]

def rand_ip():
    return f"{random.randint(10, 250)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"


def format_web_line(ip, ts, method, path, status, bytes_sent, ua):
    t = ts.strftime('%d/%b/%Y:%H:%M:%S %z')
    return f'{ip} - - [{t}] "{method} {path} HTTP/1.1" {status} {bytes_sent} "-" "{ua}"'


def format_auth_line(ts, host, pid, user, ip, success=False):
    t = ts.strftime('%b %d %H:%M:%S')
    if success:
        return f"{t} {host} sshd[{pid}]: Accepted password for {user} from {ip} port 22"
    return f"{t} {host} sshd[{pid}]: Failed password for invalid user {user} from {ip} port 22"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out-dir', default='logs', help='output directory')
    ap.add_argument('--web-lines', type=int, default=5000)
    ap.add_argument('--auth-lines', type=int, default=1500)
    ap.add_argument('--system-lines', type=int, default=800)
    ap.add_argument('--seed', type=int, default=42)
    ap.add_argument('--bruteforce-rate', type=float, default=0.12)
    ap.add_argument('--ddos-rate', type=float, default=0.08)
    ap.add_argument('--sqli-rate', type=float, default=0.05)
    ap.add_argument('--xss-rate', type=float, default=0.05)
    args = ap.parse_args()

    random.seed(args.seed)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now().astimezone()
    start = now - timedelta(hours=2)

    # Pick attacker IPs
    brute_ip = rand_ip()
    ddos_ip = rand_ip()
    sqli_ip = rand_ip()
    xss_ip = rand_ip()

    # Web logs
    web_lines = []
    for i in range(args.web_lines):
        ts = start + timedelta(seconds=random.randint(0, 7200))
        ip = rand_ip()
        method = random.choice(METHODS)
        path = random.choice(WEB_PATHS)
        status = random.choice(STATUS_CODES)
        bytes_sent = random.randint(200, 5000)
        ua = random.choice(USER_AGENTS)

        # Inject DDoS bursts
        if random.random() < args.ddos_rate:
            ip = ddos_ip

        # Inject SQLi
        if random.random() < args.sqli_rate:
            ip = sqli_ip
            path = f"/search?q={random.choice(SQLI_PATTERNS)}"
            status = 200

        # Inject XSS
        if random.random() < args.xss_rate:
            ip = xss_ip
            path = f"/profile?bio={random.choice(XSS_PATTERNS)}"
            status = 200

        web_lines.append(format_web_line(ip, ts, method, path, status, bytes_sent, ua))

    # Auth logs
    auth_lines = []
    host = "client-node"
    for i in range(args.auth_lines):
        ts = start + timedelta(seconds=random.randint(0, 7200))
        ip = rand_ip()
        user = random.choice(USERS)
        pid = random.randint(1000, 9999)

        # Inject brute-force attempts
        if random.random() < args.bruteforce_rate:
            ip = brute_ip
            user = random.choice(USERS)
            auth_lines.append(format_auth_line(ts, host, pid, user, ip, success=False))
            continue

        # Normal mix of success/fail
        success = random.random() < 0.2
        auth_lines.append(format_auth_line(ts, host, pid, user, ip, success=success))

    (out_dir / 'web.log').write_text("\n".join(web_lines) + "\n")
    (out_dir / 'auth.log').write_text("\n".join(auth_lines) + "\n")

    # System logs
    system_lines = []
    for i in range(args.system_lines):
        ts = start + timedelta(seconds=random.randint(0, 7200))
        t = ts.strftime('%b %d %H:%M:%S')
        msg_tpl = random.choice(SYSTEM_MESSAGES)
        msg = msg_tpl.format(ip=rand_ip(), cid=random.randint(1000, 9999))
        system_lines.append(f"{t} {host} {msg}")
    (out_dir / 'system.log').write_text("\n".join(system_lines) + "\n")

    print(f"Generated {len(web_lines)} web lines, {len(auth_lines)} auth lines, and {len(system_lines)} system lines in {out_dir}")
    print(f"Attack IPs: brute={brute_ip}, ddos={ddos_ip}, sqli={sqli_ip}, xss={xss_ip}")


if __name__ == '__main__':
    main()

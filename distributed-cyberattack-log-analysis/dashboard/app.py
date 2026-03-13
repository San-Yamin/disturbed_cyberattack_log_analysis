#!/usr/bin/env python3
import csv
import json
import os
from collections import defaultdict
from datetime import datetime
from flask import Flask, render_template_string

APP = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPORT_DIR = os.getenv("REPORT_DIR", os.path.join(BASE_DIR, "server", "reports"))
ALERTS_TSV = os.getenv("ALERTS_TSV", os.path.join(REPORT_DIR, "alerts_latest.tsv"))

TEMPLATE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Distributed Cyberattack Log Analysis Dashboard</title>
  <style>
    :root {
      --bg: #f2f4f7;
      --card: #ffffff;
      --text: #111827;
      --muted: #6b7280;
      --border: #e5e7eb;
      --accent: #1d79d6;
      --accent-2: #38bdf8;
      --danger: #ea580c;
      --danger-bg: #fff4ed;
    }
    [data-theme="dark"] {
      --bg: #0f172a;
      --card: #111827;
      --text: #e5e7eb;
      --muted: #9ca3af;
      --border: #1f2937;
      --accent: #38bdf8;
      --accent-2: #60a5fa;
      --danger: #f97316;
      --danger-bg: #2a1b12;
    }
    * { box-sizing: border-box; }
    body { font-family: "Helvetica Neue", Arial, sans-serif; margin: 0; background: var(--bg); color: var(--text); }
    .page { max-width: 1200px; margin: 0 auto; padding: 22px; }
    h1, h2, h3 { margin: 0 0 8px 0; font-weight: 700; }
    h1 { font-size: 26px; letter-spacing: 0.2px; }
    h2 { font-size: 18px; margin-top: 8px; }
    .muted { color: var(--muted); font-size: 13px; }
    .header { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 16px 18px; display: flex; justify-content: space-between; align-items: center; gap: 16px; }
    .title-block p { margin: 4px 0 0 0; }
    .toggle { border: 1px solid var(--border); background: transparent; padding: 6px 10px; border-radius: 8px; cursor: pointer; color: var(--text); }
    .grid { display: grid; gap: 16px; }
    .kpis { grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); margin-top: 14px; }
    .card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 14px 16px; }
    .kpi-title { font-size: 12px; text-transform: uppercase; letter-spacing: 0.06em; color: var(--muted); margin-bottom: 6px; }
    .kpi-value { font-size: 22px; font-weight: 700; color: var(--accent); }
    .kpi-sub { font-size: 12px; color: var(--muted); margin-top: 4px; }
    .section { margin-top: 16px; }
    .tables { grid-template-columns: 1.2fr 1fr; }
    .table-wrap { max-height: 280px; overflow: auto; border: 1px solid var(--border); border-radius: 10px; }
    table { border-collapse: collapse; width: 100%; }
    th, td { padding: 8px 10px; text-align: left; font-size: 13px; border-bottom: 1px solid var(--border); }
    th { position: sticky; top: 0; background: var(--card); z-index: 1; }
    tr:nth-child(even) { background: rgba(0,0,0,0.02); }
    [data-theme="dark"] tr:nth-child(even) { background: rgba(255,255,255,0.03); }
    .tag { display: inline-block; padding: 2px 6px; border-radius: 999px; font-size: 11px; background: #e8f3ff; color: var(--accent); }
    .alert-row { background: var(--danger-bg); }
    .alert-badge { color: var(--danger); font-weight: 600; }
    .charts { grid-template-columns: 1fr 1fr; }
    .bar-row { display: flex; align-items: center; gap: 10px; margin: 8px 0; }
    .bar-label { width: 120px; font-size: 13px; }
    .bar { height: 10px; background: linear-gradient(90deg, var(--accent), var(--accent-2)); border-radius: 6px; }
    .bar-track { flex: 1; background: #e5eef9; border-radius: 6px; overflow: hidden; height: 10px; }
    .pie { width: 180px; height: 180px; border-radius: 50%; background: conic-gradient({{ pie_gradient }}); margin: 12px auto; border: 1px solid var(--border); }
    .legend { display: grid; gap: 6px; font-size: 12px; }
    .legend-item { display: flex; align-items: center; gap: 6px; }
    .dot { width: 10px; height: 10px; border-radius: 50%; }
    .footer { margin-top: 18px; padding: 10px 12px; border-radius: 10px; border: 1px dashed var(--border); background: var(--card); display: grid; gap: 4px; font-size: 12px; color: var(--muted); }
    .caption { font-size: 12px; color: var(--muted); margin-top: 4px; }
  </style>
</head>
<body data-theme="light">
  <div class="page">
    <div class="header">
      <div class="title-block">
        <h1>Distributed Cyberattack Log Analysis Dashboard</h1>
        <p class="muted">Academic, rule‑based security analytics using Hadoop Streaming (Python)</p>
      </div>
      <button class="toggle" onclick="toggleTheme()">Toggle dark mode</button>
    </div>

    <div class="grid kpis">
      <div class="card">
        <div class="kpi-title">Total Logs Processed</div>
        <div class="kpi-value">{{ kpis.total_logs }}</div>
        <div class="kpi-sub">From HDFS (summary report)</div>
      </div>
      <div class="card">
        <div class="kpi-title">Total Attacks Detected</div>
        <div class="kpi-value">{{ kpis.total_attacks }}</div>
        <div class="kpi-sub">Sum of alert counts</div>
      </div>
      <div class="card">
        <div class="kpi-title">Most Frequent Attack</div>
        <div class="kpi-value">{{ kpis.top_attack }}</div>
        <div class="kpi-sub">Highest attack count</div>
      </div>
      <div class="card">
        <div class="kpi-title">Top Attacking IP</div>
        <div class="kpi-value">{{ kpis.top_ip }}</div>
        <div class="kpi-sub">Highest total events</div>
      </div>
    </div>

    <div class="grid charts section">
      <div class="card">
        <h2>Attack Type vs Count</h2>
        <div class="caption">Bar chart of total detected events per attack type.</div>
        {% if attack_counts %}
          {% for attack, count, pct in attack_bars %}
            <div class="bar-row">
              <div class="bar-label">{{ attack }}</div>
              <div class="bar-track"><div class="bar" style="width: {{ pct }}%"></div></div>
              <div class="muted">{{ count }}</div>
            </div>
          {% endfor %}
        {% else %}
          <p class="muted">No data yet. Run MapReduce jobs and export alerts.</p>
        {% endif %}
      </div>
      <div class="card">
        <h2>Attack Distribution</h2>
        <div class="caption">Pie chart of proportional attack distribution.</div>
        {% if attack_counts %}
          <div class="pie"></div>
          <div class="legend">
            {% for item in pie_legend %}
              <div class="legend-item"><span class="dot" style="background: {{ item.color }}"></span>{{ item.label }} ({{ item.count }})</div>
            {% endfor %}
          </div>
        {% else %}
          <p class="muted">No data yet. Run MapReduce jobs and export alerts.</p>
        {% endif %}
      </div>
    </div>

    <div class="grid tables section">
      <div class="card">
        <h2>Attack Counts</h2>
        <div class="caption">Aggregated counts from MapReduce output.</div>
        <div class="table-wrap">
          <table>
            <tr><th>Attack Type</th><th>Count</th></tr>
            {% for attack, count in attack_counts %}
              <tr>
                <td><span class="tag">{{ attack }}</span></td>
                <td>{{ count }}</td>
              </tr>
            {% endfor %}
          </table>
        </div>
      </div>

      <div class="card">
        <h2>Top Attacking IPs</h2>
        <div class="caption">Ranked by total attack events.</div>
        <div class="table-wrap">
          <table>
            <tr><th>IP Address</th><th>Count</th></tr>
            {% for ip, count in top_ips %}
              <tr><td>{{ ip }}</td><td>{{ count }}</td></tr>
            {% endfor %}
          </table>
        </div>
      </div>
    </div>

    <div class="card section">
      <h2>Latest Alerts (First 100)</h2>
      <div class="caption">Red/orange highlights indicate critical attack activity.</div>
      <div class="table-wrap" style="max-height: 340px;">
        <table>
          <tr><th>Type</th><th>IP</th><th>Count</th><th>First</th><th>Last</th></tr>
          {% for row in alerts %}
            <tr class="{{ 'alert-row' if row['highlight'] else '' }}">
              <td class="{{ 'alert-badge' if row['highlight'] else '' }}">{{ row['type'] }}</td>
              <td>{{ row['ip'] }}</td>
              <td>{{ row['count'] }}</td>
              <td>{{ row['first'] }}</td>
              <td>{{ row['last'] }}</td>
            </tr>
          {% endfor %}
        </table>
      </div>
    </div>

    <div class="footer">
      <div>Data source: {{ alerts_path }}</div>
      <div>Last updated: {{ last_updated }}</div>
      <div>Hadoop job reference: MapReduce Streaming (Auth + Web) — /alerts/auth, /alerts/web</div>
    </div>
  </div>

  <script>
    function toggleTheme() {
      const body = document.body;
      body.dataset.theme = body.dataset.theme === "dark" ? "light" : "dark";
    }
  </script>
</body>
</html>
"""


def load_alerts(path):
    alerts = []
    attack_counts = defaultdict(int)
    ip_counts = defaultdict(int)
    if not os.path.exists(path):
        return alerts, [], [], attack_counts, ip_counts
    with open(path, newline="", encoding="utf-8") as f:
        tsv = csv.reader(f, delimiter="\t")
        for row in tsv:
            if len(row) < 6:
                continue
            _, attack_type, ip, count, first, last = row[:6]
            count = int(count)
            alerts.append({
                "type": attack_type,
                "ip": ip,
                "count": count,
                "first": first,
                "last": last,
                "highlight": attack_type in {"DDOS", "BRUTE_FORCE"} and count >= 50
            })
            attack_counts[attack_type] += count
            ip_counts[ip] += count
    alerts = alerts[:100]
    top_ips = sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    attack_counts_sorted = sorted(attack_counts.items(), key=lambda x: x[1], reverse=True)
    return alerts, attack_counts_sorted, top_ips, attack_counts, ip_counts


def load_summary(report_dir):
    path = os.path.join(report_dir, "summary_report.json")
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def build_pie_gradient(attack_counts_sorted):
    if not attack_counts_sorted:
        return "#e5e7eb 0 100%"
    total = sum(count for _, count in attack_counts_sorted) or 1
    colors = ["#1d79d6", "#38bdf8", "#0ea5e9", "#6366f1", "#f97316", "#ef4444"]
    parts = []
    start = 0.0
    for i, (label, count) in enumerate(attack_counts_sorted):
        pct = (count / total) * 100.0
        end = start + pct
        color = colors[i % len(colors)]
        parts.append(f"{color} {start:.2f}% {end:.2f}%")
        start = end
    return ", ".join(parts)


@APP.route("/")
def index():
    alerts, attack_counts_sorted, top_ips, attack_counts_map, ip_counts_map = load_alerts(ALERTS_TSV)
    summary = load_summary(REPORT_DIR) or {}
    total_logs = summary.get("total_logs_processed", "N/A")
    total_attacks = sum(attack_counts_map.values())
    top_attack = attack_counts_sorted[0][0] if attack_counts_sorted else "N/A"
    top_ip = top_ips[0][0] if top_ips else "N/A"

    # bar chart data (percent of max)
    max_count = max((c for _, c in attack_counts_sorted), default=1)
    attack_bars = [(a, c, int((c / max_count) * 100)) for a, c in attack_counts_sorted]

    # pie chart data
    pie_gradient = build_pie_gradient(attack_counts_sorted)
    colors = ["#1d79d6", "#38bdf8", "#0ea5e9", "#6366f1", "#f97316", "#ef4444"]
    pie_legend = []
    for i, (label, count) in enumerate(attack_counts_sorted):
        pie_legend.append({"label": label, "count": count, "color": colors[i % len(colors)]})

    # last updated timestamp
    if os.path.exists(ALERTS_TSV):
        ts = datetime.fromtimestamp(os.path.getmtime(ALERTS_TSV))
        last_updated = ts.strftime("%Y-%m-%d %H:%M:%S")
    else:
        last_updated = "N/A"

    return render_template_string(
        TEMPLATE,
        alerts=alerts,
        attack_counts=attack_counts_sorted,
        attack_bars=attack_bars,
        top_ips=top_ips,
        alerts_path=ALERTS_TSV,
        last_updated=last_updated,
        pie_gradient=pie_gradient,
        pie_legend=pie_legend,
        kpis={
            "total_logs": total_logs,
            "total_attacks": total_attacks,
            "top_attack": top_attack,
            "top_ip": top_ip,
        }
    )


if __name__ == "__main__":
    # Changed port to 5001 to avoid macOS AirPlay conflict
    APP.run(host="0.0.0.0", port=5001, debug=True)

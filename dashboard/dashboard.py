import sqlite3

print("Running dashboard...")

conn = sqlite3.connect("siem.db")
cursor = conn.cursor()

# Total logs
cursor.execute("SELECT COUNT(*) FROM logs")
total_logs = cursor.fetchone()[0]

# Failed logins
cursor.execute("SELECT COUNT(*) FROM logs WHERE event_type='LOGIN_FAILED'")
failed_logs = cursor.fetchone()[0]

# Top attackers
cursor.execute("""
SELECT ip_address, COUNT(*)
FROM logs
WHERE event_type='LOGIN_FAILED'
GROUP BY ip_address
ORDER BY COUNT(*) DESC
LIMIT 5
""")
top_attackers = cursor.fetchall()

# Recent alerts
cursor.execute("""
SELECT timestamp, ip_address
FROM logs
WHERE event_type='LOGIN_FAILED'
ORDER BY id DESC
LIMIT 5
""")
recent_alerts = cursor.fetchall()

conn.close()

# HTML START
html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Mini SIEM Dashboard</title>
    <meta http-equiv="refresh" content="5">

    <style>
        body {{
            font-family: Arial;
            background: #0d1117;
            color: white;
            padding: 20px;
        }}

        h1 {{
            color: #00ffcc;
        }}

        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .container {{
            display: flex;
            gap: 20px;
            margin-top: 20px;
        }}

        .card {{
            background: #161b22;
            padding: 20px;
            border-radius: 10px;
            flex: 1;
        }}

        .card p {{
            font-size: 28px;
            color: #00ffcc;
        }}

        .section {{
            margin-top: 20px;
            background: #161b22;
            padding: 20px;
            border-radius: 10px;
        }}

        li {{
            margin: 8px 0;
        }}

        .attacker {{
            color: #ff4d4d;
        }}

        .alert {{
            color: orange;
        }}
    </style>
</head>

<body>

<div class="header">
    <h1>Mini SIEM Dashboard</h1>
    <p style="color:gray;">Live Monitoring</p>
</div>

<div class="container">
    <div class="card">
        <h2>Total Logs</h2>
        <p>{total_logs}</p>
    </div>

    <div class="card">
        <h2>Failed Logins</h2>
        <p>{failed_logs}</p>
    </div>
</div>

<div class="section">
    <h2>Top Attackers</h2>
    <ul>
"""

# Add attackers
for ip, count in top_attackers:
    html += f"<li class='attacker'>{ip} -> {count} attempts</li>"

html += """
    </ul>
</div>

<div class="section">
    <h2>Recent Alerts</h2>
    <ul>
"""

# Add alerts
for time, ip in recent_alerts:
    html += f"<li class='alert'>{time} - Suspicious login from {ip}</li>"

html += """
    </ul>
</div>

</body>
</html>
"""

# Save file
with open("dashboard/dashboard.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Dashboard created successfully")
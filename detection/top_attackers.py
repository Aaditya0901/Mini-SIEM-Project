import sqlite3

conn = sqlite3.connect("siem.db")
cursor = conn.cursor()

print("\nTop Attacking IPs:\n")

cursor.execute("""
SELECT ip_address, COUNT(*) as attempts
FROM logs
WHERE event_type = 'LOGIN_FAILED'
GROUP BY ip_address
ORDER BY attempts DESC
""")

rows = cursor.fetchall()

for ip, count in rows:
    print(f"{ip} → {count} failed attempts")

conn.close()
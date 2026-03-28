import sqlite3

# Connect to SQLite (auto-creates file)
conn = sqlite3.connect("siem.db")
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    event_type TEXT,
    username TEXT,
    ip_address TEXT
)
""")

# Read logs
with open("logs/system.log", "r") as file:
    lines = file.readlines()

# Insert logs
for line in lines:
    parts = line.split()

    timestamp = parts[0] + " " + parts[1]
    event = parts[2]
    user = parts[3].split("=")[1]
    ip = parts[4].split("=")[1]

    cursor.execute(
        "INSERT INTO logs (timestamp, event_type, username, ip_address) VALUES (?, ?, ?, ?)",
        (timestamp, event, user, ip)
    )

conn.commit()
conn.close()

print("Logs stored in SQLite database (siem.db)")
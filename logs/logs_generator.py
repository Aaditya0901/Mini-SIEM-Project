#This script simulates system logs. 
# It generates random login events for a set of users and IP addresses, and writes them to a log file.
# The logs include a timestamp, the event type (login success or failure), the username, and the IP address.
# The script runs indefinitely, generating a new log entry every 2 seconds.
import random 
import time

users = ["admin", "user1", "user2"]
ips = ["192.168.1.10", "192.168.1.15", "192.168.1.20"]

events = ["LOGIN_SUCCESS", "LOGIN_FAILED"]

while True:
    user = random.choice(users)
    ip = random.choice(ips)
    event = random.choice(events)

    log = f"{time.strftime('%Y-%m-%d %H:%M:%S')} {event} user={user} ip={ip}"

    with open("logs/system.log", "a") as f:
        f.write(log + "\n")

    print(log)

    time.sleep(2)
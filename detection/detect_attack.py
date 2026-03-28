#alert once per attacker.
#When an IP fails login 5 times, it prints an alert.
#Then it stores that IP in alerted_ips.
#After that, it will not alert again for that same IP.
#This script continuously monitors the system log file for failed login attempts.
#It counts the number of failed attempts from each IP address and raises an alert if an IP address has 5 or more failed attempts.
#Once an alert is raised for an IP address, it will not raise another alert for that same IP address to avoid spamming.
import time

failed_attempts = {}
alerted_ips = set()

while True:
    with open("logs/system.log", "r") as file:
        lines = file.readlines()

    for line in lines:
        if "LOGIN_FAILED" in line:

            parts = line.split("ip=")
            ip = parts[1].strip()

            failed_attempts[ip] = failed_attempts.get(ip, 0) + 1

            if failed_attempts[ip] >= 5 and ip not in alerted_ips:
                print(f"ALERT: Possible Brute Force Attack from {ip}")
                alerted_ips.add(ip)

    time.sleep(5)
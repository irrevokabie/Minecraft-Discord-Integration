import requests
import time
import re

webhook_url = ""
log_path = ""
chat_regex = re.compile(r"<(.+?)> (.+)")
lines_read = set()

def send_webhook(username, message):
    embed = {
        "title": username,
        "description": f"`{message}`",
        "color": 3066993
    }

    response = requests.post(webhook_url, json={"embeds": [embed]})
    if response.status_code != 204:
        print(f"{response.status_code} : {response.text}")

def mc_log():
    with open(log_path, "r", encoding="utf-8") as file:
        file.seek(0, 2)
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.1)
                continue
            if line in lines_read:
                continue
            lines_read.add(line)
            match = chat_regex.search(line)
            if match:
                username, message = match.groups()
                send_webhook(username, message)

if __name__ == "__main__":
    mc_log()

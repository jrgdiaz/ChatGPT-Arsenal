import json
import requests
from bs4 import BeautifulSoup
import schedule
import time
import smtplib

# function to retrieve targets from web server
def get_targets():
    try:
        # send HTTP GET request to retrieve JSON file
        r = requests.get("http://example.com/targets.json")
        # parse JSON file
        targets = json.loads(r.text)
        return targets
    except Exception as e:
        print(f"Error retrieving targets from web server: {e}")
        return None

# function to perform banner grabbing and HTML title extraction on target
def http_banner_grab(target):
    try:
        # send HTTP GET request
        r = requests.get(f"http://{target}")
        # extract banner from response
        banner = r.headers["Server"]
        soup = BeautifulSoup(r.content, 'html.parser')
        title = soup.title.string
        print(f"Banner grabbed successfully from {target}")
        print(f"Title: {title}")
        return banner, title
    except Exception as e:
        print(f"Error performing banner grabbing on {target}: {e}")
        return None, None

# function to send email notification
def send_email_notification(banner, title, target):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("YOUR_EMAIL@gmail.com", "YOUR_PASSWORD")

        msg = f"Banner: {banner}\nTitle: {title}\nTarget: {target}"
        server.sendmail("SENDER_EMAIL@gmail.com", "RECIPIENT_EMAIL@gmail.com", msg)
        print(f"Email notification sent to recipient for {target}")
        server.quit()
    except Exception as e:
        print(f"Error sending email notification: {e}")

# function to perform banner grabbing on all targets
def perform_banner_grab():
    targets = get_targets()
    if targets:
        for target in targets:
            banner, title = http_banner_grab(target)
            if banner and title:
                send_email_notification(banner, title, target)

# schedule the retrieval of updated targets every 24 hours
schedule.every().day.at("00:00").do(get_targets)

while True:
    schedule.run_pending()
    time.sleep(1)

import os
import requests

MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
EMAIL_TO = os.getenv("EMAIL_TO")

def send_mailgun_email(new_jobs):
    if not (MAILGUN_API_KEY and MAILGUN_DOMAIN and EMAIL_TO):
        print("❌ Environment variables not loaded properly.")
        print(f"MAILGUN_API_KEY: {bool(MAILGUN_API_KEY)}")
        print(f"MAILGUN_DOMAIN: {MAILGUN_DOMAIN}")
        print(f"EMAIL_TO: {EMAIL_TO}")
        return

    message = "\n".join(new_jobs)
    print("🚨 New jobs found:")
    print(message)

    url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"
    response = requests.post(
        url,
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": f"Job Watcher <postmaster@{MAILGUN_DOMAIN}>",
            "to": EMAIL_TO,
            "subject": "🚨 New jobs posted",
            "text": message
        }
    )

    if response.status_code == 200:
        print("✅ Email sent successfully via Mailgun.")
    else:
        print(f"❌ Failed to send email. Status: {response.status_code}")
        print(response.text)


# For testing only — mock job list
if __name__ == "__main__":
    mock_jobs = [
        "https://example.com/job/123",
        "https://example.com/job/456"
    ]
    send_mailgun_email(mock_jobs)

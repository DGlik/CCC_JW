import requests
import os
from bs4 import BeautifulSoup

MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
EMAIL_TO = os.getenv("EMAIL_TO")
EMAIL_FROM = f"Job Scraper <mailgun@{MAILGUN_DOMAIN}>"

WORKDAY_URL = "https://foundationccc.wd1.myworkdayjobs.com/fccc-careers"

def scrape_jobs():
    response = requests.get(WORKDAY_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    job_links = []

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if href.startswith("/fccc-careers/job"):
            full_url = f"https://foundationccc.wd1.myworkdayjobs.com{href}"
            if full_url not in job_links:
                job_links.append(full_url)

    return job_links


def send_email(job_links):
    if not job_links:
        print("✅ No new jobs found.")
        return

    body = "🚨 New jobs found:\n\n" + "\n".join(job_links)

    response = requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": EMAIL_FROM,
            "to": EMAIL_TO,
            "subject": "New Job Postings Found",
            "text": body,
        },
    )

    if response.status_code == 200:
        print("✅ Email sent successfully via Mailgun.")
    else:
        print(f"❌ Failed to send email. Status: {response.status_code}")
        print(response.text)


if __name__ == "__main__":
    jobs = scrape_jobs()
    print("🔍 Jobs scraped:", len(jobs))
    send_email(jobs)

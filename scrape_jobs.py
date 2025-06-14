import asyncio
import os
import json
import requests
from email.utils import formatdate
from playwright.async_api import async_playwright

WORKDAY_URL = "https://foundationccc.wd1.myworkdayjobs.com/fccc-careers"
SEEN_FILE = "seen_jobs.json"

MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")
MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")
EMAIL_TO = os.environ.get("EMAIL_TO")
EMAIL_FROM = f"Job Bot <mailgun@{MAILGUN_DOMAIN}>"


def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return json.load(f)
    return []


def save_seen(jobs):
    with open(SEEN_FILE, "w") as f:
        json.dump(jobs, f)


def send_email(new_jobs):
    subject = f"[TopShot] New Job(s) Posted at FoundationCCC"
    body = "\n\n".join(new_jobs)

    data = {
        "from": EMAIL_FROM,
        "to": EMAIL_TO,
        "subject": subject,
        "text": f"New job listings:\n\n{body}",
    }

    response = requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data=data,
    )

    if response.status_code == 200:
        print(f"✅ Email sent to {EMAIL_TO} with {len(new_jobs)} new job(s)")
    else:
        print(f"❌ Failed to send email. Status: {response.status_code}")
        print(response.text)


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(WORKDAY_URL)
        await page.wait_for_load_state("networkidle")

        job_links = await page.eval_on_selector_all(
            "a[href*='/fccc-careers/']", "els => els.map(e => e.href)"
        )
        await browser.close()

        unique_links = sorted(set(job_links))
        seen_links = load_seen()

        new_jobs = [link for link in unique_links if link not in seen_links]

        if new_jobs:
            print("🚨 New jobs found:")
            for job in new_jobs:
                print(job)
            send_email(new_jobs)
        else:
            print("✅ No new jobs found.")

        save_seen(unique_links)


if __name__ == "__main__":
    asyncio.run(main())

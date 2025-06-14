import asyncio
import smtplib
import os
import json
from email.message import EmailMessage
from playwright.async_api import async_playwright

WORKDAY_URL = "https://foundationccc.wd1.myworkdayjobs.com/fccc-careers"
SEEN_FILE = "seen_jobs.json"

EMAIL_USER = os.environ.get("GMAIL_APP_LOGIN")
EMAIL_PASS = os.environ.get("GMAIL_APP_PASS")
EMAIL_TO = EMAIL_USER  # change this if you want to send to a different address


def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return json.load(f)
    return []


def save_seen(jobs):
    with open(SEEN_FILE, "w") as f:
        json.dump(jobs, f)


def send_email(new_jobs):
    subject = "New FoundationCCC Job(s) Posted"
    body = "\n\n".join(new_jobs)

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO
    msg.set_content(f"New job listings:\n\n{body}")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)

    print(f"✅ Email sent with {len(new_jobs)} job(s)")


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

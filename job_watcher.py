import requests
import json
from datetime import datetime

url = 'https://foundationccc.wd1.myworkdayjobs.com/wday/cxs/foundationccc/fccc-careers/jobs'
headers = {
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0',
    'Content-Type': 'application/json'
}

def load_seen_jobs():
    try:
        with open("seen_jobs.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_seen_jobs(jobs):
    with open("seen_jobs.json", "w") as f:
        json.dump(jobs, f)

def main():
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print(f"Request failed: {r.status_code}")
        return

    data = r.json()
    job_postings = data.get("jobPostings", [])
    seen = load_seen_jobs()

    new_jobs = []
    for job in job_postings:
        link = 'https://foundationccc.wd1.myworkdayjobs.com/fccc-careers' + job.get('externalPath', '')
        if link not in seen:
            new_jobs.append(link)

    if new_jobs:
        print("New jobs found:")
        for job in new_jobs:
            print(job)
        save_seen_jobs([job['externalPath'] for job in job_postings])
    else:
        print(f"No new jobs. Last checked: {datetime.now()}")

if __name__ == "__main__":
    main()

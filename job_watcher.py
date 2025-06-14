import requests, json, os
from datetime import datetime

URL = 'https://foundationccc.wd1.myworkdayjobs.com/wday/cxs/foundationccc/fccc-careers/jobs'

HEADERS = {
    # what Workday expects from a real browser
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.9',
    'Content-Type': 'application/json',
    'Origin': 'https://foundationccc.wd1.myworkdayjobs.com',
    'Referer': 'https://foundationccc.wd1.myworkdayjobs.com/fccc-careers'
}

SEEN_FILE = 'seen_jobs.json'          # lives in the repo

def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, 'r') as f:
            return json.load(f)
    return []

def save_seen(urls):
    with open(SEEN_FILE, 'w') as f:
        json.dump(urls, f)

def main():
    r = requests.get(URL, headers=HEADERS)
    if r.status_code != 200:
        print(f'Request failed: {r.status_code}')
        print(r.text)
        return

    data = r.json()
    postings = data.get('jobPostings', [])
    current_urls = [
        'https://foundationccc.wd1.myworkdayjobs.com/fccc-careers' + p['externalPath']
        for p in postings
    ]

    seen = load_seen()
    new_jobs = [url for url in current_urls if url not in seen]

    if new_jobs:
        print('NEW JOBS FOUND:')
        for url in new_jobs:
            print(url)
    else:
        print(f'No new jobs – {datetime.utcnow().isoformat()}')

    save_seen(current_urls)

if __name__ == '__main__':
    main()

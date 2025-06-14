import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        url = "https://foundationccc.wd1.myworkdayjobs.com/fccc-careers"
        await page.goto(url)
        await page.wait_for_load_state("networkidle")

        job_links = await page.eval_on_selector_all(
            "a[href*='/fccc-careers/']", "elements => elements.map(e => e.href)"
        )

        unique_links = sorted(set(job_links))
        print("FOUND JOBS:")
        for link in unique_links:
            print(link)

        await browser.close()

asyncio.run(main())

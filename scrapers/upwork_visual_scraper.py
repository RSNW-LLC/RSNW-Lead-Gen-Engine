import csv
import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

TARGET_URL = "https://www.upwork.com/freelance-jobs/web-scraping/"
OUTPUT_FILE = "data_outputs/upwork_live_buyers.csv"

async def brute_force_upwork():
    print(f"[*] Deploying headless browser against Upwork: {TARGET_URL}")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        try:
            await page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=60000)
            print("[*] Waiting for UI to render...")
            await page.wait_for_timeout(3000)
            
            html = await page.content()
            soup = BeautifulSoup(html, 'html.parser')
            
            jobs = []
            # Upwork SEO pages wrap job titles in specific section tags
            job_cards = soup.find_all('section', class_='up-card-section')
            
            for card in job_cards:
                title_elem = card.find('h2') or card.find('h3')
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    jobs.append({"buyer_request": title, "platform": "Upwork"})
                    
            if jobs:
                with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=["buyer_request", "platform"])
                    writer.writeheader()
                    writer.writerows(jobs)
                print(f"[✓] Captured {len(jobs)} live contracts. Saved to {OUTPUT_FILE}")
            else:
                print("[X] Extraction failed. Upwork WAF may have blocked the headless browser.")
                
        except Exception as e:
            print(f"[X] Browser failure: {e}")
            
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(brute_force_upwork())

import asyncio
import os
import csv
import sys
import random
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

TARGET_URL = "https://www.thumbtack.com/pro-leads/opportunities"
OUTPUT_FILE = "data_outputs/thumbtack_leads.csv"
# Allow passing a custom auth state filename as an argument
AUTH_STATE = sys.argv[1] if len(sys.argv) > 1 else "auth_state.json"

async def human_delay(min_sec=2, max_sec=5):
    delay = random.uniform(min_sec, max_sec)
    await asyncio.sleep(delay)

async def get_thumbtack_leads():
    print(f"[*] Initializing Thumbtack Opportunity Scraper using session: {AUTH_STATE}")
    
    async with async_playwright() as p:
        # Check if we have a saved session
        if not os.path.exists(AUTH_STATE):
            print("[!] Authentication state not found.")
            print("[*] Launching browser for manual login. Please log in to your Thumbtack Pro account.")
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto("https://www.thumbtack.com/login")
            
            print("[*] Waiting for login to complete... (Close the browser window once logged in and on the dashboard)")
            while not page.is_closed() and "opportunities" not in page.url:
                await asyncio.sleep(1)
            
            if not page.is_closed():
                await context.storage_state(path=AUTH_STATE)
                print(f"[✓] Authentication state saved to {AUTH_STATE}")
                await browser.close()
            else:
                print("[X] Browser closed before login completed.")
                return

        # Start scraping session
        print("[*] Launching headless browser with saved session...")
        browser = await p.chromium.launch(headless=True)
        # Use a consistent, high-quality user agent
        context = await browser.new_context(
            storage_state=AUTH_STATE,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        try:
            print(f"[*] Navigating to {TARGET_URL}")
            await page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=60000)
            
            # Human-like interaction: Random pause after load
            await human_delay(3, 7)
            
            # Human-like interaction: Scroll slightly to trigger lazy loading
            print("[*] Performing human-like scrolling...")
            for i in range(3):
                scroll_amount = random.randint(300, 700)
                await page.evaluate(f"window.scrollBy(0, {scroll_amount})")
                await human_delay(1, 3)
            
            html = await page.content()
            soup = BeautifulSoup(html, 'html.parser')
            
            leads = []
            # Updated selectors based on debug HTML analysis
            opportunity_cards = soup.select('[data-testid="updated-opportunity-list-item"]')
            
            for card in opportunity_cards:
                # The entire card text contains the details
                details_containers = card.select('.mw7')
                
                # Usually: 0=Location, 1=Date, 2=Job Details
                location = details_containers[0].get_text(strip=True) if len(details_containers) > 0 else "Unknown"
                job_info = details_containers[2].get_text(strip=True) if len(details_containers) > 2 else "No details"
                
                # Use the first part of the job info as the "title"
                title = job_info.split(',')[0] if ',' in job_info else job_info
                
                link = "https://www.thumbtack.com" + card['href'] if card.has_attr('href') else TARGET_URL
                
                leads.append({
                    "buyer_request": f"{title} ({location})",
                    "details": job_info,
                    "contract_link": link
                })
            
            if leads:
                with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=["buyer_request", "details", "contract_link"])
                    writer.writeheader()
                    writer.writerows(leads)
                print(f"[✓] Successfully captured {len(leads)} Thumbtack opportunities. Saved to {OUTPUT_FILE}")
            else:
                print("[X] No opportunities found. Check thumbtack_debug.html")
                with open("thumbtack_debug.html", "w", encoding="utf-8") as f:
                    f.write(html)
                
        except Exception as e:
            print(f"[X] Extraction failure: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(get_thumbtack_leads())

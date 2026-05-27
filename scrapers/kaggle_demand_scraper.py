import csv
import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

OUTPUT_FILE = "data_outputs/kaggle_data_requests.csv"
TARGET_URL = "https://www.kaggle.com/discussions/general?search=need+dataset"

async def scrape_kaggle_demand():
    print(f"[*] Targeting Kaggle Discussion Boards: {TARGET_URL}")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        page = await context.new_page()
        
        try:
            await page.goto(TARGET_URL, wait_until="networkidle", timeout=60000)
            
            print("[*] Scrolling to force JS hydration...")
            for _ in range(4):
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
                await page.wait_for_timeout(2000)
                
            html = await page.content()
            soup = BeautifulSoup(html, 'html.parser')
            
            requests = []
            links = soup.find_all('a')
            for link in links:
                title = link.get_text(strip=True)
                if len(title) > 15 and ("dataset" in title.lower() or "data" in title.lower()):
                    href = link.get('href')
                    if href and "/discussions/" in href:
                        requests.append({
                            "topic_title": title,
                            "url": f"https://www.kaggle.com{href}"
                        })
            
            unique_requests = {req['url']: req for req in requests}.values()
            
            if unique_requests:
                with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=["topic_title", "url"])
                    writer.writeheader()
                    writer.writerows(unique_requests)
                print(f"[✓] Captured {len(unique_requests)} unfulfilled demands. Saved to {OUTPUT_FILE}")
            else:
                print("[X] No requests found. Adjust search parameters or wait for market shift.")
                
        except Exception as e:
            print(f"[X] Extraction failure: {e}")
            
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_kaggle_demand())

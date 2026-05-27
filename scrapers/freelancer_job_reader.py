import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

URL = "https://www.freelancer.com/projects/beautifulsoup/Comprehensive-Business-Directory-40468852"

async def read_job():
    print(f"[*] Deploying Playwright to read target contract: {URL}")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        try:
            await page.goto(URL, wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(2000) # Wait for React UI to hydrate
            
            html = await page.content()
            soup = BeautifulSoup(html, 'html.parser')
            
            print("\n[+] BUYER REQUIREMENTS:\n")
            # Extract raw text, locate the known starting string, and print the next 1000 characters
            raw_text = soup.get_text(separator=' ', strip=True)
            start_index = raw_text.find("I'm looking for an experienced web scraper")
            
            if start_index != -1:
                print(raw_text[start_index:start_index+1000])
            else:
                print("[-] Could not isolate exact text. Printing fallback snippet:")
                print(raw_text[:1000])
                
        except Exception as e:
            print(f"[X] Browser extraction failure: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(read_job())

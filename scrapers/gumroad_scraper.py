import asyncio
import csv
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

# Search for products related to web scraping or custom data services
TARGET_URL = "https://gumroad.com/discover?query=web+scraping"
OUTPUT_FILE = "data_outputs/gumroad_leads.csv"

async def scrape_gumroad():
    print(f"[*] Targeting Gumroad Discover: {TARGET_URL}")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        try:
            # Gumroad uses heavy JS for their discover page
            await page.goto(TARGET_URL, wait_until="networkidle", timeout=60000)
            
            # Scroll down to load more products
            print("[*] Scrolling to load dynamic products...")
            for _ in range(3):
                await page.mouse.wheel(0, 2000)
                await asyncio.sleep(2)
            
            html = await page.content()
            soup = BeautifulSoup(html, 'html.parser')
            
            products = []
            # Products are usually in 'article' or 'div' with specific classes
            # Gumroad structure often uses 'product-card' classes or data-testid
            product_cards = soup.select('article') or soup.select('[class*="ProductCard"]')
            
            for card in product_cards:
                title_elem = card.find(['h2', 'h3']) or card.select_one('[class*="title"]')
                link_elem = card.find('a', href=True)
                
                if title_elem and link_elem:
                    title = title_elem.get_text(strip=True)
                    # Filter for things that look like services or high-value tools
                    link = link_elem['href']
                    if not link.startswith('http'):
                        link = "https://gumroad.com" + link
                    
                    products.append({
                        "buyer_request": f"Product/Service: {title}",
                        "platform": "Gumroad",
                        "contract_link": link
                    })
            
            if products:
                with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=["buyer_request", "platform", "contract_link"])
                    writer.writeheader()
                    writer.writerows(products)
                print(f"[✓] Captured {len(products)} Gumroad items. Saved to {OUTPUT_FILE}")
            else:
                print("[X] No items found on Gumroad. Check selector logic.")
                
        except Exception as e:
            print(f"[X] Gumroad extraction failure: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_gumroad())

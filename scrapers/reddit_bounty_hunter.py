import urllib.request
import json
import csv

# Target Reddit job requests for web scraping
URL = "https://www.reddit.com/r/webscraping/search.json?q=hiring+OR+paid+OR+job+OR+request&restrict_sr=on&sort=new&t=day"
OUTPUT_FILE = "data_outputs/reddit_bounties.csv"

def hunt_reddit():
    print("[*] Penetrating Reddit JSON endpoint...")
    # A custom User-Agent is required to bypass Reddit's default bot block
    req = urllib.request.Request(URL, headers={'User-Agent': 'RSNW_Data_Arbitrage_Node/1.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
        
        jobs = []
        for post in data['data']['children']:
            title = post['data']['title']
            url = "https://www.reddit.com" + post['data']['permalink']
            # Grab a preview of the actual job description
            text = post['data'].get('selftext', '')[:100].replace('\n', ' ')
            jobs.append({"buyer_request": title, "preview": text, "contract_link": url})
            
        if jobs:
            with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["buyer_request", "preview", "contract_link"])
                writer.writeheader()
                writer.writerows(jobs)
            print(f"[✓] Secured {len(jobs)} active buyer bounties. Saved to {OUTPUT_FILE}")
            print("[*] Top 3 urgent requests:")
            for j in jobs[:3]:
                print(f"    -> {j['buyer_request']}")
        else:
            print("[X] No active bounties found on this feed.")
            
    except Exception as e:
        print(f"[X] Feed extraction failed: {e}")

if __name__ == "__main__":
    hunt_reddit()

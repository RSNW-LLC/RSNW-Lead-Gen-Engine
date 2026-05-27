import urllib.request
import json
import csv

# Target r/slavelabour strictly for TASK posts related to scraping or data
URL = "https://www.reddit.com/r/slavelabour/search.json?q=%5BTASK%5D+AND+(scrape+OR+data+OR+python+OR+bot)&restrict_sr=on&sort=new&t=day"
OUTPUT_FILE = "data_outputs/task_buyers.csv"

def hunt_task_market():
    print("[*] Penetrating r/slavelabour JSON endpoint (7-Day Strict)...")
    req = urllib.request.Request(URL, headers={'User-Agent': 'Data_Arbitrage_Node/1.3'})
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
        
        jobs = []
        for post in data['data']['children']:
            title = post['data']['title']
            url = "https://www.reddit.com" + post['data']['permalink']
            
            # Ensure it is a paying task
            if "[task]" in title.lower():
                jobs.append({"buyer_request": title, "contract_link": url})
            
        if jobs:
            with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["buyer_request", "contract_link"])
                writer.writeheader()
                writer.writerows(jobs)
            print(f"[✓] Secured {len(jobs)} active task bounties. Saved to {OUTPUT_FILE}")
            print("[*] Top 3 fresh scraping tasks:")
            for j in jobs[:3]:
                print(f"    -> {j['buyer_request']}")
        else:
            print("[X] No scraping tasks posted on r/slavelabour this week.")
            
    except Exception as e:
        print(f"[X] Feed extraction failed: {e}")

if __name__ == "__main__":
    hunt_task_market()

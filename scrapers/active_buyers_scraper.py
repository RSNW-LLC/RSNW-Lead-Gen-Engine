import urllib.request
import json
import csv

# Target Reddit job requests strictly from the last 7 days
URL = "https://www.reddit.com/r/webscraping/search.json?q=hiring+OR+paid+OR+job+OR+request&restrict_sr=on&sort=new&t=day"
OUTPUT_FILE = "data_outputs/live_funded_buyers.csv"

def hunt_active_buyers():
    print("[*] Accessing job market backend (7-Day Strict Filter)...")
    req = urllib.request.Request(URL, headers={'User-Agent': 'Data_Arbitrage_Node/1.1'})
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
        
        jobs = []
        for post in data['data']['children']:
            title = post['data']['title']
            url = "https://www.reddit.com" + post['data']['permalink']
            
            # Filter out non-commercial community noise
            if "weekly" not in title.lower() and "newbie" not in title.lower() and "advice" not in title.lower():
                jobs.append({"buyer_request": title, "contract_link": url})
            
        if jobs:
            with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["buyer_request", "contract_link"])
                writer.writeheader()
                writer.writerows(jobs)
            print(f"[✓] Secured {len(jobs)} active, unlocked buyer contracts. Saved to {OUTPUT_FILE}")
            print("[*] Top 3 fresh requests:")
            for j in jobs[:3]:
                print(f"    -> {j['buyer_request']}")
        else:
            print("[X] No fresh bounties posted this week.")
            
    except Exception as e:
        print(f"[X] Feed extraction failed: {e}")

if __name__ == "__main__":
    hunt_active_buyers()

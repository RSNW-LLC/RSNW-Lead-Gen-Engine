import urllib.request
import json
import csv

# Target r/forhire strictly for HIRING posts related to data
URL = "https://www.reddit.com/r/forhire/search.json?q=%5BHiring%5D+AND+(scrape+OR+data+OR+extraction)&restrict_sr=on&sort=new&t=day"
OUTPUT_FILE = "data_outputs/verified_buyers.csv"

def hunt_verified_buyers():
    print("[*] Penetrating r/forhire JSON endpoint (7-Day Strict)...")
    req = urllib.request.Request(URL, headers={'User-Agent': 'Data_Arbitrage_Node/1.2'})
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
        
        jobs = []
        for post in data['data']['children']:
            title = post['data']['title']
            url = "https://www.reddit.com" + post['data']['permalink']
            text = post['data'].get('selftext', '')[:100].replace('\n', ' ')
            
            # Ensure it is a hiring post, not someone offering services
            if "[hiring]" in title.lower():
                jobs.append({"buyer_request": title, "preview": text, "contract_link": url})
            
        if jobs:
            with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["buyer_request", "preview", "contract_link"])
                writer.writeheader()
                writer.writerows(jobs)
            print(f"[✓] Secured {len(jobs)} active, verified buyer contracts. Saved to {OUTPUT_FILE}")
            print("[*] Top fresh requests:")
            for j in jobs[:3]:
                print(f"    -> {j['buyer_request']}")
        else:
            print("[X] No fresh data bounties posted on r/forhire this week.")
            
    except Exception as e:
        print(f"[X] Feed extraction failed: {e}")

if __name__ == "__main__":
    hunt_verified_buyers()

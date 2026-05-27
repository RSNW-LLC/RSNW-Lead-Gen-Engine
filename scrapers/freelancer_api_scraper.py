import urllib.request
import json
import csv

# Target the public Freelancer.com active projects API
URL = "https://www.freelancer.com/api/projects/0.1/projects/active?query=scraping&limit=15"
OUTPUT_FILE = "data_outputs/freelancer_buyers.csv"

def hunt_freelancer():
    print("[*] Penetrating Freelancer.com open API endpoint...")
    req = urllib.request.Request(URL, headers={'User-Agent': 'Data_Arbitrage_Node/2.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
        
        jobs = []
        projects = data.get('result', {}).get('projects', [])
        
        for p in projects:
            title = p.get('title', 'Unknown')
            desc = p.get('preview_description', '')[:100].replace('\n', ' ')
            seo_url = p.get('seo_url', '')
            link = f"https://www.freelancer.com/projects/{seo_url}" if seo_url else "N/A"
            
            jobs.append({"buyer_request": title, "preview": desc, "contract_link": link})
            
        if jobs:
            with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["buyer_request", "preview", "contract_link"])
                writer.writeheader()
                writer.writerows(jobs)
            print(f"[✓] Secured {len(jobs)} global buyer contracts. Saved to {OUTPUT_FILE}")
            print("[*] Top 3 urgent global requests:")
            for j in jobs[:3]:
                print(f"    -> {j['buyer_request']}")
        else:
            print("[X] No active scraping contracts found on this endpoint.")
            
    except Exception as e:
        print(f"[X] Feed extraction failed: {e}")

if __name__ == "__main__":
    hunt_freelancer()

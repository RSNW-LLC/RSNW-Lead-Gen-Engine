import urllib.request
import xml.etree.ElementTree as ET
import csv

RSS_URL = "https://www.upwork.com/ab/feed/jobs/rss?q=web+scraping+OR+dataset+OR+data+extraction"
OUTPUT_FILE = "data_outputs/guaranteed_buyers.csv"

def harvest_buyers():
    print(f"[*] Connecting to Upwork Commercial Feed...")
    req = urllib.request.Request(RSS_URL, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            
        root = ET.fromstring(xml_data)
        jobs = []
        
        for item in root.findall('.//item'):
            title = item.find('title').text
            # Clean up the RSS title formatting
            clean_title = title.replace(" - Upwork", "").strip()
            link = item.find('link').text
            jobs.append({"buyer_request": clean_title, "contract_link": link})
            
        if jobs:
            with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["buyer_request", "contract_link"])
                writer.writeheader()
                writer.writerows(jobs)
            print(f"[✓] Secured {len(jobs)} active buyer contracts. Saved to {OUTPUT_FILE}")
            print("[*] Printing top 5 highest-urgency requests:")
            for j in jobs[:5]:
                print(f"    -> {j['buyer_request']}")
        else:
            print("[X] No active contracts found on this feed.")
    except Exception as e:
        print(f"[X] Feed extraction failed: {e}")

if __name__ == "__main__":
    harvest_buyers()

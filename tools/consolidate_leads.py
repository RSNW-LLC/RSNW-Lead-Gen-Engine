import csv
import os

OUTPUT_FILE = "data_outputs/master_lead_list.csv"
SCHEMA = ["platform", "buyer_request", "description_preview", "contract_link"]

MAPPINGS = {
    "data_outputs/freelancer_buyers.csv": {
        "platform": "Freelancer",
        "map": {"buyer_request": "buyer_request", "description_preview": "preview", "contract_link": "contract_link"}
    },
    "data_outputs/kaggle_data_requests.csv": {
        "platform": "Kaggle",
        "map": {"buyer_request": "topic_title", "description_preview": None, "contract_link": "url"}
    },
    "data_outputs/live_funded_buyers.csv": {
        "platform": "Reddit (Active)",
        "map": {"buyer_request": "buyer_request", "description_preview": None, "contract_link": "contract_link"}
    },
    "data_outputs/reddit_bounties.csv": {
        "platform": "Reddit (General)",
        "map": {"buyer_request": "buyer_request", "description_preview": "preview", "contract_link": "contract_link"}
    },
    "data_outputs/task_buyers.csv": {
        "platform": "Reddit (Slavelabour)",
        "map": {"buyer_request": "buyer_request", "description_preview": None, "contract_link": "contract_link"}
    },
    "data_outputs/verified_buyers.csv": {
        "platform": "Reddit (ForHire)",
        "map": {"buyer_request": "buyer_request", "description_preview": "preview", "contract_link": "contract_link"}
    },
    "data_outputs/gumroad_leads.csv": {
        "platform": "Gumroad",
        "map": {"buyer_request": "buyer_request", "description_preview": None, "contract_link": "contract_link"}
    },
    "data_outputs/thumbtack_leads.csv": {
        "platform": "Thumbtack",
        "map": {"buyer_request": "buyer_request", "description_preview": "details", "contract_link": "contract_link"}
    },
    "data_outputs/guaranteed_buyers.csv": {
        "platform": "Upwork (RSS)",
        "map": {"buyer_request": "buyer_request", "description_preview": None, "contract_link": "contract_link"}
    },
    "data_outputs/upwork_live_buyers.csv": {
        "platform": "Upwork (Visual)",
        "map": {"buyer_request": "buyer_request", "description_preview": None, "contract_link": None}
    }
}

def consolidate():
    print("[*] Starting Lead Consolidation...")
    all_leads = []
    
    for filename, config in MAPPINGS.items():
        if not os.path.exists(filename):
            continue
            
        print(f"[*] Processing {filename}...")
        try:
            with open(filename, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    lead = {"platform": config["platform"]}
                    for target_field, source_field in config["map"].items():
                        if source_field and source_field in row:
                            lead[target_field] = row[source_field]
                        else:
                            lead[target_field] = ""
                    all_leads.append(lead)
        except Exception as e:
            print(f"[X] Error processing {filename}: {e}")

    if all_leads:
        # Sort by platform then request
        all_leads.sort(key=lambda x: (x['platform'], x['buyer_request']))
        
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=SCHEMA)
            writer.writeheader()
            writer.writerows(all_leads)
        print(f"\n[✓] CONSOLIDATION COMPLETE: {len(all_leads)} total leads saved to {OUTPUT_FILE}")
    else:
        print("\n[X] No lead data found to consolidate.")

if __name__ == "__main__":
    consolidate()

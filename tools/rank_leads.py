import duckdb
import pandas as pd
import os

# The database file created by dlt
DB_FILE = "intelligence_db/lead_intelligence_pipeline.duckdb"

# User's target locations
PRIMARY_LOCATIONS = ["shelton", "98584", "grapeview", "98546"]
SECONDARY_LOCATIONS = ["belfair", "98528", "port orchard", "98366", "bremerton", "98312", "wa"]

def rank_leads():
    print(f"[*] Connecting to Lead Intelligence Database: {DB_FILE}")
    if not os.path.exists(DB_FILE):
        print(f"[X] Error: Database {DB_FILE} not found. Run the master pipeline first.")
        return
        
    try:
        con = duckdb.connect(DB_FILE)
    except Exception as e:
        print(f"[X] Could not connect to database: {e}")
        return

    # Query all leads from the leads_data schema and all_leads table
    try:
        df = con.execute("SELECT platform, buyer_request, description_preview, contract_link FROM leads_data.all_leads").df()
    except Exception as e:
        print(f"[X] Query failed: {e}")
        print("[!] Make sure you have run 'python3 master_runner.py' first.")
        return

    def calculate_rank(row):
        text = (str(row['buyer_request']) + " " + str(row['description_preview'])).lower()
        platform = str(row['platform']).lower()
        
        # Level 1: Free Scraping/Tech Leads (Reddit/Kaggle)
        # These are prioritized because they don't require a card/fees
        if "reddit" in platform or "kaggle" in platform:
            if any(k in text for k in ["scrape", "data", "python", "bot"]):
                return 1, "High Value (Free)"
        
        # Level 2: Hyper-Local (Thumbtack)
        for loc in PRIMARY_LOCATIONS:
            if loc in text:
                return 2, "Hyper-Local"
        
        # Level 3: Local (Thumbtack)
        for loc in SECONDARY_LOCATIONS[:6]: 
            if loc in text:
                return 3, "Local (Kitsap/Mason)"
        
        # Level 4: Other Free Leads (General Reddit)
        if "reddit" in platform or "kaggle" in platform:
            return 4, "General (Free)"
        
        # Level 5: Regional Thumbtack
        if " wa" in text or ", wa" in text:
            return 5, "Regional (WA State)"
            
        # Level 6: Everything else
        return 6, "Remote/Global"

    print(f"[*] Ranking {len(df)} leads...")
    df[['rank_score', 'rank_label']] = df.apply(lambda r: pd.Series(calculate_rank(r)), axis=1)
    
    # Sort by rank score (lowest is best)
    df_sorted = df.sort_values('rank_score')

    print("\n" + "="*80)
    print(f"{'RANK':<15} | {'PLATFORM':<15} | {'LEAD TITLE'}")
    print("-"*80)
    
    for _, row in df_sorted.iterrows():
        print(f"{row['rank_label']:<15} | {row['platform']:<15} | {row['buyer_request'][:50]}")
    
    print("="*80)
    
    # Export to a specialized CSV
    df_sorted.to_csv("RANKED_LEADS_DOWLOAD.csv", index=False)
    print(f"\n[✓] Ranked list saved to 'RANKED_LEADS_DOWLOAD.csv'")
    
    # Summary
    counts = df['rank_label'].value_counts()
    print("\nSummary of Opportunities:")
    for label, count in counts.items():
        print(f" - {label}: {count}")

if __name__ == "__main__":
    rank_leads()

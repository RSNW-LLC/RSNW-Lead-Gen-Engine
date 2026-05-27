import os
import subprocess
import sys
import time

# Add the tools directory to the path so we can import the helpers
sys.path.append(os.path.join(os.getcwd(), 'tools'))

from consolidate_leads import consolidate
from leads_to_db import load_leads_to_duckdb
from rank_leads import rank_leads

# List of functional scrapers to run (now located in the scrapers/ folder)
SCRAPERS = [
    "active_buyers_scraper.py",
    "freelancer_api_scraper.py",
    "gumroad_scraper.py",
    "kaggle_demand_scraper.py",
    "reddit_bounty_hunter.py",
    "targeted_buyer_scraper.py",
    "task_market_scraper.py",
    # "thumbtack_scraper.py",
    "upwork_demand_harvester.py",
    "upwork_visual_scraper.py"
]

def run_scraper(script_name):
    print(f"\n{'='*60}")
    print(f"[*] LAUNCHING: {script_name}")
    print(f"{'='*60}")

    script_path = os.path.join("scrapers", script_name)

    start_time = time.time()
    try:
        # Run the script as a subprocess using the current python interpreter
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=False, # We want to see the output in real-time
            text=True,
            check=False # Don't raise exception on non-zero exit to continue with others
        )

        duration = time.time() - start_time
        if result.returncode == 0:
            print(f"\n[✓] {script_name} completed successfully in {duration:.2f}s")
        else:
            print(f"\n[X] {script_name} failed with exit code {result.returncode} after {duration:.2f}s")

    except Exception as e:
        print(f"\n[!] Critical error running {script_name}: {e}")


def main():
    print("RSNW LeadGen Master Runner")
    print("==========================")
    print(f"Found {len(SCRAPERS)} scrapers to execute.")
    
    for scraper in SCRAPERS:
        script_path = os.path.join("scrapers", scraper)
        if os.path.exists(script_path):
            run_scraper(scraper)
        else:
            print(f"\n[!] Warning: Scraper script '{script_path}' not found. Skipping.")
            
    # Consolidate all results into a master list
    print("\n" + "="*60)
    consolidate()
    
    # Load into Lead Intelligence Database (DuckDB)
    print("\n" + "="*60)
    load_leads_to_duckdb()
    
    # Rank leads by location
    print("\n" + "="*60)
    rank_leads()
    
    print("="*60)
    print("[*] ALL SCRAPERS, CONSOLIDATION, DB LOAD, AND RANKING EXECUTED.")
    print("[*] Open 'ranked_leads.csv' to download your new opportunities.")
    print("="*60)

if __name__ == "__main__":
    main()

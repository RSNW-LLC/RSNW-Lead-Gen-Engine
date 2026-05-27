import duckdb
import os
from collections import Counter
import re

DB_FILE = "intelligence_db/lead_intelligence_pipeline.duckdb"

# List of keywords we want to track
SKILLS_TO_TRACK = [
    "python", "javascript", "react", "scraping", "automation", 
    "sql", "api", "data entry", "excel", "bot", "ai", "machine learning"
]

def analyze_trends():
    print("[*] Analyzing market trends in your database...")
    if not os.path.exists(DB_FILE):
        print("[X] Database not found.")
        return
        
    con = duckdb.connect(DB_FILE)
    
    try:
        # Get all job titles and descriptions
        rows = con.execute("SELECT buyer_request, description_preview FROM leads_data.all_leads").fetchall()
    except Exception as e:
        print(f"[X] Query failed: {e}")
        return

    # Flatten all text
    big_text = " ".join([str(r[0]) + " " + str(r[1]) for r in rows]).lower()
    
    # Count occurrences of our target skills
    results = {}
    for skill in SKILLS_TO_TRACK:
        count = len(re.findall(rf'\b{skill}\b', big_text))
        if count > 0:
            results[skill] = count

    # Sort results
    sorted_trends = sorted(results.items(), key=lambda item: item[1], reverse=True)

    print("\n" + "!"*40)
    print("      CURRENT HOT SKILLS (Based on your leads)")
    print("!"*40)
    for skill, count in sorted_trends:
        bar = "█" * (count if count < 20 else 20)
        print(f"{skill.upper():<15} : {count} mentions {bar}")
    print("!"*40)
    print("\n[PRO TIP] Focus your learning and pitches on the top 3 skills above.")

if __name__ == "__main__":
    analyze_trends()

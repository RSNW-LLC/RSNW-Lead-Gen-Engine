import duckdb
import ollama
import os

# Database file
DB_FILE = "intelligence_db/lead_intelligence_pipeline.duckdb"

def generate_pitches():
    print("[*] Connecting to Lead Intelligence Database...")
    if not os.path.exists(DB_FILE):
        print("[X] Database not found. Run the master_runner first.")
        return
        
    con = duckdb.connect(DB_FILE)
    
    # Get the top 3 leads (prioritizing high-value ones)
    try:
        # We join with our ranking logic if possible, or just take the latest
        query = "SELECT platform, buyer_request, description_preview, contract_link FROM leads_data.all_leads LIMIT 3"
        leads = con.execute(query).fetchall()
    except Exception as e:
        print(f"[X] Query failed: {e}")
        return

    print(f"[*] Generating AI Pitches for {len(leads)} leads...\n")

    for i, lead in enumerate(leads):
        platform, title, desc, link = lead
        
        prompt = f"""
        Act as a professional freelancer. Write a 3-sentence 'hook' or pitch for the following job:
        Title: {title}
        Description: {desc}
        Platform: {platform}
        
        The pitch should be:
        1. Professional but energetic.
        2. Highlight expertise in Python and Automation.
        3. End with a call to action.
        """
        
        try:
            response = ollama.generate(model='llama3', prompt=prompt)
            print(f"--- LEAD #{i+1}: {title} ---")
            print(f"URL: {link}")
            print(f"PITCH:\n{response['response']}\n")
        except Exception as e:
            print(f"[X] AI Error on lead {i+1}: {e}")

if __name__ == "__main__":
    generate_pitches()

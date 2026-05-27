# 📖 THE RSNW BOOK OF SCRIPTS
*Your Secret Weapons for Lead Generation and Automation*

---

## 🛰️ THE HUNTERS (Scrapers)
*Location: `/scrapers/`*

### 1. `master_runner.py` (The General)
**What it does:** The "One Button" to rule them all. It starts every scraper, cleans the data, saves it to the database, and ranks it.
**How to use:** `python3 master_runner.py`

### 2. `thumbtack_scraper.py` (The Local Scout)
**What it does:** Logs into your Thumbtack Pro account (stealthily) and grabs new job opportunities.
**Weapon Status:** Finds high-paying local work (Plumbing, Handyman, etc.).

### 3. `reddit_bounty_hunter.py` (The Social Sniper)
**What it does:** Scours Reddit for people asking for "Hiring" or "Paid Tasks" in the last 24 hours.
**Weapon Status:** Best for finding "Free" leads (no bidding fees).

---

## 🧠 THE BRAIN (Data & Intelligence)
*Location: `/tools/` and `/intelligence_db/`*

### 4. `consolidate_leads.py` (The Librarian)
**What it does:** Takes the 10 different files from the scrapers and merges them into one master list.

### 5. `leads_to_db.py` (The Vault)
**What it does:** Moves your leads into a "DuckDB" database. 
**Weapon Status:** Keeps your leads safe forever. Even if you delete a CSV, the data is in the Vault.

### 6. `rank_leads.py` (The GPS)
**What it does:** Looks at your home address (Shelton/Grapeview) and automatically moves local jobs to the top of your list.

---

## 🕵️ THE STEALTH TOOLS (Security)
*Location: `/tools/`*

### 7. `WinSystemTimer.py` (The Invisible Assistant)
**What it does:** Watches a part of your screen and sends the text to your phone for AI answers.
**Weapon Status:** 100% undetectable. Use this to win "Live Coding" tests or complex tasks on Outlier/Prolific.

### 8. `system_monitor.py` (The Ghost)
**What it does:** A simpler version of the Assistant that stays inside your terminal.

---

## 🧹 HOUSEKEEPING
### 9. `organize_my_laptop.py` (The Janitor)
**What it does:** Automatically cleans up your messy folders (Downloads/Desktop) and puts things where they belong.
**How to use:** `python3 tools/organize_my_laptop.py`

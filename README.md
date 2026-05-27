# RSNW Lead Generation & Intelligence Engine

An autonomous, multi-platform data pipeline designed to discover, rank, and notify high-value business opportunities in real-time.

## 🚀 Overview
This system orchestrates a fleet of custom scrapers across multiple professional platforms, consolidates the data into a high-performance analytical database, and uses AI-driven ranking to identify the best "hot" leads for immediate action.

## 🏗️ Architecture & Data Flow
The engine is built on a modular "Collect-Normalize-Analyze" architecture:

1.  **Multi-Platform Orchestration**: A master Python controller manages 10+ specialized scrapers (Reddit, Freelancer, Kaggle, Thumbtack, Gumroad).
    *   Uses **Playwright** for dynamic JS-heavy sites.
    *   Implements **advanced session management** (auth state persistence) to bypass login walls.
    *   Features **"humanized" behavior** (randomized delays/scrolling) to evade bot detection.
2.  **Professional Data Engineering**:
    *   Leverages the **DLT (Data Load Tool)** framework to ingest disparate CSV data into a unified schema.
    *   Utilizes **DuckDB** as a local OLAP database for sub-millisecond querying of thousands of leads.
3.  **Intelligence & Ranking Layer**:
    *   Custom algorithms rank leads based on **Geographical Proximity** (Mason/Kitsap/WA State).
    *   Keywords-based scoring identifies "High Value" scraping and automation jobs.
4.  **Invisible Side-Car Assistant**:
    *   A background daemon using **OCR (Tesseract)** to monitor screen regions.
    *   Integrated **Flask Web Server** to bridge AI-generated solutions to a secondary device (Phone/Tablet) for 100% stealth during screen-shared tasks.

## 🛠️ Tech Stack
*   **Languages**: Python 3.13+
*   **Scraping**: Playwright, BeautifulSoup4, urllib
*   **Database**: DuckDB, DLT
*   **AI Integration**: Ollama (Llama3), Tesseract OCR
*   **Web Framework**: Flask
*   **Operating System**: Kali Linux / Debian

## 📂 Project Structure
*   `/scrapers`: Individual worker bots for each platform.
*   `/tools`: Intelligence layer, database management, and stealth services.
*   `/data_outputs`: Raw lead data and consolidated reports.
*   `/intelligence_db`: The permanent DuckDB lead store.
*   `master_runner.py`: The central execution hub.

---
**Developed by Reliable Solutions Northwest**

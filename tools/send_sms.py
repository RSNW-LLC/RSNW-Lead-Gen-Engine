import smtplib
from email.mime.text import MIMEText
import pandas as pd
import os

# Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "reliablesolutionsnorthwest@gmail.com"
# The App Password provided by the user
SENDER_PASSWORD = "rifm lfem dady cruo" 
RECIPIENT_SMS = "3607646501@vtext.com"

def send_sms_alerts():
    print("[*] Checking for new high-priority local leads to notify...")
    
    ranked_file = "ranked_leads.csv"
    if not os.path.exists(ranked_file):
        print("[X] Ranked leads file not found. Run ranking first.")
        return

    df = pd.read_csv(ranked_file)
    
    # Filter for High Value Free (Scraping), Hyper-Local, and Local leads
    priority_labels = ['High Value (Free)', 'Hyper-Local', 'Local (Kitsap/Mason)']
    priority_leads = df[df['rank_label'].isin(priority_labels)]
    
    if priority_leads.empty:
        print("[*] No new high-priority leads found. No SMS sent.")
        return

    print(f"[*] Found {len(priority_leads)} priority leads. Preparing SMS dispatch...")
    
    # Sort by rank score to ensure the absolute best are first in the text
    priority_leads = priority_leads.sort_values('rank_score')

    # Compose the message
    message_body = "RSNW Priority Leads:\n"
    # Take the top 5 to give you a good mix
    for _, lead in priority_leads.head(5).iterrows(): 
        title = lead['buyer_request'][:25]
        link = lead['contract_link']
        # Add the platform name so you know if it's Reddit or Thumbtack
        platform = lead['platform'].split('(')[0].strip()
        message_body += f"[{platform}] {title} {link}\n"

    try:
        # Create the email/SMS message
        msg = MIMEText(message_body)
        msg["Subject"] = "Lead Alert"
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECIPIENT_SMS

        # Connect and send
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            
        print(f"[✓] SMS Notification sent to {RECIPIENT_SMS}")
    except Exception as e:
        print(f"[X] Failed to send SMS: {e}")

if __name__ == "__main__":
    send_sms_alerts()

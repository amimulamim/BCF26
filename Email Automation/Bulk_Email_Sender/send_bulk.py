#!/usr/bin/env python3
"""
Bulk Email Sender via Brevo
Main sending script - edit config.py to customize settings.

Usage:
    python send_bulk.py form_response.csv
"""

import os
import sys
import time
import pandas as pd
import requests
from datetime import datetime, timezone

# Import configuration
import config


# ========================================
# CONSTANTS (from config)
# ========================================
BREVO_API_KEY = config.BREVO_API_KEY or os.getenv("BREVO_API_KEY", "").strip()
BREVO_URL = "https://api.brevo.com/v3/smtp/email"


# ========================================
# HELPER FUNCTIONS
# ========================================

def clean_email(x) -> str:
    """Clean and normalize email address"""
    return str(x).strip().lower() if pd.notna(x) else ""


def now_iso() -> str:
    """Return current timestamp in ISO format"""
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def send_email_brevo(to_email: str, team: str) -> tuple[bool, str]:
    """
    Send email via Brevo API
    
    Args:
        to_email: Recipient email address
        team: Team name
    
    Returns:
        (success: bool, info: str) - info is messageId or error message
    """
    if not BREVO_API_KEY:
        return False, "Missing BREVO_API_KEY"
    
    # Get message from env or config
    message = os.getenv("EMAIL_MESSAGE", config.DEFAULT_MESSAGE)
    
    payload = {
        "sender": {"name": config.FROM_NAME, "email": config.FROM_EMAIL},
        "to": [{"email": to_email, "name": team}],
        "replyTo": {"name": config.REPLY_TO_NAME, "email": config.REPLY_TO_EMAIL},
        "subject": config.SUBJECT,
        "textContent": config.BODY_TEXT_TEMPLATE.format(
            team=team,
            message=message,
            reply_team=config.REPLY_TO_NAME
        )
    }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": BREVO_API_KEY
    }
    
    try:
        r = requests.post(BREVO_URL, json=payload, headers=headers, timeout=30)
        
        if 200 <= r.status_code < 300:
            try:
                msg_id = r.json().get("messageId", "OK")
            except Exception:
                msg_id = "OK"
            return True, msg_id
        else:
            try:
                error_msg = r.json().get("message", r.text)
            except Exception:
                error_msg = r.text
            return False, f"HTTP {r.status_code}: {error_msg}"
    
    except requests.exceptions.Timeout:
        return False, "Request timeout"
    except requests.exceptions.RequestException as e:
        return False, f"Request error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"


# ========================================
# MAIN PROCESSING
# ========================================

def main():
    """Process CSV and send bulk emails"""
    
    # Get CSV path from command line or use default
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "form_response.csv"
    
    if not os.path.exists(csv_path):
        print(f"❌ Error: File not found: {csv_path}")
        sys.exit(1)
    
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        sys.exit(1)
    
    # Ensure tracking columns exist
    if config.SEND_NOW_COL not in df.columns:
        df[config.SEND_NOW_COL] = ""
    if config.MAIL_SENT_COL not in df.columns:
        df[config.MAIL_SENT_COL] = ""
    
    if config.EMAIL_COL not in df.columns:
        print(f"❌ Error: Missing column '{config.EMAIL_COL}' in CSV")
        sys.exit(1)
    
    # Clean columns
    df["_to_email"] = df[config.EMAIL_COL].apply(clean_email)
    
    if config.TEAM_COL in df.columns:
        df["_team"] = df[config.TEAM_COL].fillna("Team").astype(str).str.strip()
    else:
        df["_team"] = "Team"
    
    # Only send where Send Now = YES and Mail Sent is empty
    send_mask = (
        df[config.SEND_NOW_COL].astype(str).str.upper().str.strip() == "YES"
    ) & (
        (df[config.MAIL_SENT_COL].isna()) | 
        (df[config.MAIL_SENT_COL].astype(str).str.strip() == "")
    )
    
    candidates = df[send_mask].copy()
    candidates = candidates[candidates["_to_email"] != ""]
    candidates = candidates.drop_duplicates(subset=["_to_email"])
    
    print("="*50)
    print("📧 Bulk Email Sender")
    print("="*50)
    print(f"📄 Loaded: {len(df)} rows from {csv_path}")
    print(f"➡️  Will send: {len(candidates)} emails (Send Now=YES & Mail Sent empty)")
    
    if config.TEST_MODE:
        print(f"⚠️  TEST MODE: All emails will go to {config.TEST_TO}")
    
    if len(candidates) == 0:
        print("\n✨ No emails to send!")
        return
    
    print()
    
    sent_count = 0
    fail_count = 0
    
    for idx, row in candidates.iterrows():
        real_to = config.TEST_TO if config.TEST_MODE else row["_to_email"]
        team = row["_team"] or "Team"
        
        print(f"📤 Sending to: {team} <{real_to}>", end=" ")
        
        ok, info = send_email_brevo(real_to, team)
        
        if ok:
            sent_count += 1
            df.at[idx, config.MAIL_SENT_COL] = f"{now_iso()} | <{info}>"
            print(f"✅ Sent (ID: {info})")
        else:
            fail_count += 1
            print(f"❌ Failed: {info}")
        
        # Save progress after each email (safe for reruns)
        df.to_csv(csv_path, index=False)
        
        # Rate limiting (don't delay after last email)
        if idx != candidates.index[-1]:
            time.sleep(config.SECONDS_BETWEEN_EMAILS)
    
    # Summary
    print("\n" + "="*50)
    print("📊 SUMMARY")
    print("="*50)
    print(f"✅ Successfully sent: {sent_count}")
    print(f"❌ Failed: {fail_count}")
    print(f"📧 Total processed: {sent_count + fail_count}")
    
    if config.TEST_MODE:
        print(f"⚠️  TEST MODE was enabled")


# ========================================
# MAIN ENTRY POINT
# ========================================

if __name__ == "__main__":
    if not BREVO_API_KEY:
        print("❌ Error: BREVO_API_KEY not set")
        print("   Set it in config.py OR as environment variable")
        sys.exit(1)
    
    main()
    print("\n✨ Done!")

#!/usr/bin/env python3
"""
Send emails via Brevo with CC recipients support.
Main sending script - edit config.py to customize settings.

Usage:
    python send_with_cc.py recipients.csv
"""

import os
import sys
import time
import pandas as pd
import requests
from datetime import datetime, timezone
from typing import List, Dict, Tuple, Optional

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

def clean_email(email: str) -> str:
    """Clean and normalize email address"""
    return str(email).strip().lower() if pd.notna(email) and email else ""


def parse_cc_emails(cc_string: str) -> List[Dict[str, str]]:
    """
    Parse comma-separated CC emails into Brevo format
    
    Args:
        cc_string: Comma or semicolon separated emails
    
    Returns:
        List of dicts with 'email' key for Brevo API
    """
    if not cc_string or pd.isna(cc_string):
        return []
    
    emails = [clean_email(e) for e in str(cc_string).replace(';', ',').split(',')]
    return [{"email": e} for e in emails if e]


def now_iso() -> str:
    """Return current timestamp in ISO format"""
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def send_email_brevo(
    to_email: str,
    to_name: str,
    cc_emails: List[Dict[str, str]],
    team: str = "",
    custom_message: Optional[str] = None
) -> Tuple[bool, str]:
    """
    Send email via Brevo API with CC support
    
    Args:
        to_email: Primary recipient email
        to_name: Primary recipient name
        cc_emails: List of CC recipients
        team: Team name (optional)
        custom_message: Custom message to override default (optional)
    
    Returns:
        (success: bool, info: str) - info is messageId or error message
    """
    if not BREVO_API_KEY:
        return False, "Missing BREVO_API_KEY"
    
    # Use custom message or default
    message = custom_message or os.getenv("EMAIL_MESSAGE", config.DEFAULT_MESSAGE)
    
    # Build email payload
    payload = {
        "sender": {
            "name": config.FROM_NAME,
            "email": config.FROM_EMAIL
        },
        "to": [{"email": to_email, "name": to_name}],
        "replyTo": {
            "name": config.REPLY_TO_NAME,
            "email": config.REPLY_TO_EMAIL
        },
        "subject": config.SUBJECT,
        "textContent": config.BODY_TEXT_TEMPLATE.format(
            recipient_name=to_name,
            team=team,
            message=message,
            reply_team=config.REPLY_TO_NAME,
            contact_email=config.REPLY_TO_EMAIL
        )
    }
    
    # Add CC recipients if provided
    if cc_emails:
        payload["cc"] = cc_emails
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": BREVO_API_KEY
    }
    
    try:
        response = requests.post(BREVO_URL, json=payload, headers=headers, timeout=30)
        
        if 200 <= response.status_code < 300:
            try:
                msg_id = response.json().get("messageId", "OK")
            except Exception:
                msg_id = "OK"
            return True, msg_id
        else:
            try:
                error_msg = response.json().get("message", response.text)
            except Exception:
                error_msg = response.text
            return False, f"HTTP {response.status_code}: {error_msg}"
    
    except requests.exceptions.Timeout:
        return False, "Request timeout"
    except requests.exceptions.RequestException as e:
        return False, f"Request error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"


# ========================================
# MAIN PROCESSING
# ========================================

def process_csv(csv_path: str) -> None:
    """Process CSV file and send emails with CC"""
    
    if not os.path.exists(csv_path):
        print(f"❌ Error: File not found: {csv_path}")
        sys.exit(1)
    
    try:
        df = pd.read_csv(csv_path)
        print(f"📄 Loaded {len(df)} rows from {csv_path}")
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        sys.exit(1)
    
    # Validate required columns
    required_cols = [
        config.RECIPIENT_EMAIL_COL,
        config.RECIPIENT_NAME_COL,
        config.SEND_NOW_COL
    ]
    
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        print(f"❌ Missing required columns: {missing_cols}")
        print(f"   Available columns: {list(df.columns)}")
        sys.exit(1)
    
    # Add optional columns if missing
    if config.MAIL_SENT_COL not in df.columns:
        df[config.MAIL_SENT_COL] = ""
    if config.CC_EMAILS_COL not in df.columns:
        df[config.CC_EMAILS_COL] = ""
    if config.TEAM_COL not in df.columns:
        df[config.TEAM_COL] = ""
    
    # Filter rows to send
    df["_send_now_clean"] = df[config.SEND_NOW_COL].astype(str).str.strip().str.upper()
    to_send = df[df["_send_now_clean"] == "YES"].copy()
    
    print(f"📧 Found {len(to_send)} emails marked for sending")
    
    if config.TEST_MODE:
        print(f"⚠️  TEST MODE: All emails will go to {config.TEST_TO}")
    
    if config.GLOBAL_CC_EMAILS:
        print(f"📋 Global CC: {', '.join(config.GLOBAL_CC_EMAILS)}")
    
    # Counters
    sent_count = 0
    error_count = 0
    
    # Process each row
    for idx, row in to_send.iterrows():
        recipient_email = clean_email(row[config.RECIPIENT_EMAIL_COL])
        recipient_name = str(row[config.RECIPIENT_NAME_COL]).strip()
        team = str(row.get(config.TEAM_COL, "")).strip()
        cc_string = str(row.get(config.CC_EMAILS_COL, "")).strip()
        
        # Validate recipient email
        if not recipient_email or "@" not in recipient_email:
            print(f"⚠️  Row {idx}: Invalid email '{recipient_email}' - skipping")
            error_count += 1
            continue
        
        # Parse CC emails from CSV
        cc_emails = parse_cc_emails(cc_string)
        
        # Add global CC emails
        for global_cc in config.GLOBAL_CC_EMAILS:
            if global_cc and {"email": clean_email(global_cc)} not in cc_emails:
                cc_emails.append({"email": clean_email(global_cc)})
        
        # In test mode, override recipient
        actual_to = config.TEST_TO if config.TEST_MODE else recipient_email
        
        # Display info
        cc_info = f" + {len(cc_emails)} CC" if cc_emails else ""
        print(f"\n📤 Sending to: {recipient_name} <{actual_to}>{cc_info}")
        if cc_emails and not config.TEST_MODE:
            cc_list = ", ".join([e["email"] for e in cc_emails])
            print(f"   CC: {cc_list}")
        if team:
            print(f"   Team: {team}")
        
        # Send email
        success, info = send_email_brevo(
            to_email=actual_to,
            to_name=recipient_name,
            cc_emails=cc_emails if not config.TEST_MODE else [],
            team=team
        )
        
        if success:
            sent_count += 1
            timestamp_info = f"{now_iso()} | <{info}>"
            df.at[idx, config.MAIL_SENT_COL] = timestamp_info
            print(f"   ✅ Sent successfully (ID: {info})")
        else:
            error_count += 1
            print(f"   ❌ Failed: {info}")
        
        # Rate limiting
        if idx != to_send.index[-1]:
            time.sleep(config.SECONDS_BETWEEN_EMAILS)
    
    # Save updated CSV
    try:
        df.drop(columns=["_send_now_clean"], inplace=True, errors="ignore")
        df.to_csv(csv_path, index=False)
        print(f"\n💾 Updated CSV saved to {csv_path}")
    except Exception as e:
        print(f"\n⚠️  Warning: Could not save CSV: {e}")
    
    # Summary
    print(f"\n" + "="*50)
    print(f"📊 SUMMARY")
    print(f"="*50)
    print(f"✅ Successfully sent: {sent_count}")
    print(f"❌ Errors: {error_count}")
    print(f"📧 Total processed: {sent_count + error_count}")


# ========================================
# MAIN ENTRY POINT
# ========================================

if __name__ == "__main__":
    print("="*50)
    print("📧 Brevo Email Sender with CC Support")
    print("="*50)
    
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "recipients.csv"
    
    if not BREVO_API_KEY:
        print("❌ Error: BREVO_API_KEY not set")
        print("   Set it in config.py OR as environment variable")
        sys.exit(1)
    
    process_csv(csv_path)
    print("\n✨ Done!")

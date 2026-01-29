#!/usr/bin/env python3
"""
DL Sprint 4.0 - Online Round Start Notification
Sends one email per team with members in CC.

Usage:
    python send_dlsprint_start.py --test    # Test mode: only send to "Team_Test for Organizers"
    python send_dlsprint_start.py           # Send to all teams
"""

import os
import sys
import json
import time
import argparse
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load .env file from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# ========================================
# CONFIGURATION
# ========================================
BREVO_API_KEY = os.getenv("BREVO_API_KEY", "").strip()
BREVO_URL = "https://api.brevo.com/v3/smtp/email"

# Sender info
FROM_EMAIL = "noreply@buetcsefest2026.com"
FROM_NAME = "BUET CSE Fest 2026"
REPLY_TO_EMAIL = "dlsprint@buetcsefest2026.com"
REPLY_TO_NAME = "DL Sprint 4.0"

# Rate limiting
SECONDS_BETWEEN_EMAILS = 0.5

# Competition links - UPDATE THESE
KAGGLE_LINK_1 = "https://www.kaggle.com/competitions/COMPETITION_1"
KAGGLE_LINK_2 = "https://www.kaggle.com/competitions/COMPETITION_2"
RULEBOOK_LINK = "https://tinyurl.com/DLSprint4Rulebook"

# Test team name
TEST_TEAM_NAME = "Team_Test for Organizers"

# Email subject
SUBJECT = "🚀 DL Sprint 4.0 Online Round Has Started!! | BUET CSE Fest 2026"

# Email body template (HTML)
EMAIL_BODY = """\
<html>
<body>
<p>Dear Team <strong>{team_name}</strong>,</p>

<p>Greetings from BUET CSE Fest 2026!</p>

<p>We are thrilled to announce that the <strong>DL Sprint 4.0 Online Round</strong> has officially started! 🎉</p>

<p>📅 <strong>Competition Duration:</strong> 20 Days</p>

<p>🔗 <strong>Kaggle Competition Links:</strong></p>
<ul>
  <li>Competition 1: <a href="{kaggle_link_1}">{kaggle_link_1}</a></li>
  <li>Competition 2: <a href="{kaggle_link_2}">{kaggle_link_2}</a></li>
</ul>

<p>📖 <strong>Rulebook:</strong> <a href="{rulebook_link}">{rulebook_link}</a></p>

<p>Please make sure to:</p>
<ul>
  <li>✅ Read the rulebook carefully before starting</li>
  <li>✅ Join both Kaggle competitions using the links above</li>
  <li>✅ Submit your solutions before the deadline</li>
</ul>

<p>We wish you the best of luck! May the best models win! 🏆</p>

<p>If you have any questions or face any issues, feel free to reply to this email.</p>

<p>Best regards,<br>
DL Sprint 4.0 Team<br>
BUET CSE Fest 2026<br>
<a href="https://buetcsefest2026.com">buetcsefest2026.com</a><br>
<a href="mailto:dlsprint@buetcsefest2026.com">dlsprint@buetcsefest2026.com</a>
</p>
</body>
</html>
"""


def now_iso() -> str:
    """Return current timestamp in ISO format"""
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def send_email_with_cc(to_email: str, cc_emails: list, team_name: str) -> tuple[bool, str]:
    """
    Send email via Brevo API with CC recipients
    
    Args:
        to_email: Primary recipient email address
        cc_emails: List of CC email addresses
        team_name: Team name
    
    Returns:
        (success: bool, info: str) - info is messageId or error message
    """
    if not BREVO_API_KEY:
        return False, "Missing BREVO_API_KEY"
    
    # Build email body
    body = EMAIL_BODY.format(
        team_name=team_name,
        kaggle_link_1=KAGGLE_LINK_1,
        kaggle_link_2=KAGGLE_LINK_2,
        rulebook_link=RULEBOOK_LINK
    )
    
    payload = {
        "sender": {"name": FROM_NAME, "email": FROM_EMAIL},
        "to": [{"email": to_email, "name": team_name}],
        "replyTo": {"name": REPLY_TO_NAME, "email": REPLY_TO_EMAIL},
        "subject": SUBJECT,
        "htmlContent": body
    }
    
    # Add CC if there are additional members
    if cc_emails:
        payload["cc"] = [{"email": email} for email in cc_emails]
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": BREVO_API_KEY
    }
    
    try:
        r = requests.post(BREVO_URL, json=payload, headers=headers, timeout=30)
        
        if 200 <= r.status_code < 300:
            msg_id = r.json().get("messageId", "OK")
            return True, msg_id
        else:
            return False, f"HTTP {r.status_code}: {r.text}"
    except Exception as e:
        return False, str(e)


def main():
    parser = argparse.ArgumentParser(description="DL Sprint 4.0 Online Round Start Notification")
    parser.add_argument("--test", action="store_true", help="Test mode: only send to test team")
    args = parser.parse_args()
    
    # Check API key
    if not BREVO_API_KEY:
        print("❌ ERROR: BREVO_API_KEY environment variable not set")
        sys.exit(1)
    
    # Load team emails
    json_file = "team_emails.json"
    if not os.path.exists(json_file):
        print(f"❌ ERROR: {json_file} not found. Run generate_team_emails_json.py first.")
        sys.exit(1)
    
    with open(json_file, 'r', encoding='utf-8') as f:
        teams = json.load(f)
    
    # Filter for test mode
    if args.test:
        teams = [t for t in teams if t['team_name'] == TEST_TEAM_NAME]
        if not teams:
            print(f"❌ ERROR: Test team '{TEST_TEAM_NAME}' not found in {json_file}")
            sys.exit(1)
        print(f"🧪 TEST MODE: Only sending to '{TEST_TEAM_NAME}'")
    else:
        print(f"📧 PRODUCTION MODE: Sending to ALL {len(teams)} teams")
        confirm = input("Type 'yes' to confirm: ")
        if confirm.lower() != 'yes':
            print("Aborted.")
            sys.exit(0)
    
    print(f"\n{'='*60}")
    print(f"DL Sprint 4.0 - Online Round Start Notification")
    print(f"{'='*60}")
    print(f"Started at: {now_iso()}")
    print(f"Teams to process: {len(teams)}")
    print(f"{'='*60}\n")
    
    # Stats
    success_count = 0
    fail_count = 0
    
    for i, team in enumerate(teams, 1):
        team_name = team['team_name']
        emails = team['emails']
        
        if not emails:
            print(f"[{i}/{len(teams)}] ⚠️  {team_name}: No emails found, skipping")
            continue
        
        # First email is TO, rest are CC
        to_email = emails[0]
        cc_emails = emails[1:] if len(emails) > 1 else []
        
        print(f"[{i}/{len(teams)}] 📤 {team_name}")
        print(f"    TO: {to_email}")
        if cc_emails:
            print(f"    CC: {', '.join(cc_emails)}")
        
        success, info = send_email_with_cc(to_email, cc_emails, team_name)
        
        if success:
            print(f"    ✅ Sent (ID: {info})")
            success_count += 1
        else:
            print(f"    ❌ Failed: {info}")
            fail_count += 1
        
        # Rate limiting
        if i < len(teams):
            time.sleep(SECONDS_BETWEEN_EMAILS)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Successful: {success_count}")
    print(f"❌ Failed: {fail_count}")
    print(f"Finished at: {now_iso()}")


if __name__ == "__main__":
    main()

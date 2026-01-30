#!/usr/bin/env python3
"""
DL Sprint 4.0 - Send Emails to NEW Teams Only

This script handles the complete workflow:
1. Detects new teams from the latest CSV
2. Sends emails to new teams only
3. Automatically marks them as sent

Usage:
    python send_to_new_teams.py --check     # Just show new teams (dry run)
    python send_to_new_teams.py --test      # Send only to test team
    python send_to_new_teams.py             # Send to all new teams
"""

import os
import sys
import json
import time
import argparse
import requests
import pandas as pd
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load .env file from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# ========================================
# FILE CONFIGURATION
# ========================================
CSV_FILE = "DL Sprint Team Registration Form (Responses) - Form responses 1_new.csv"
SENT_LOG_FILE = "sent_teams.json"

# ========================================
# EMAIL CONFIGURATION
# ========================================
BREVO_API_KEY = os.getenv("BREVO_API_KEY", "").strip()
BREVO_URL = "https://api.brevo.com/v3/smtp/email"

FROM_EMAIL = "noreply@buetcsefest2026.com"
FROM_NAME = "BUET CSE Fest 2026"
REPLY_TO_EMAIL = "dlsprint@buetcsefest2026.com"
REPLY_TO_NAME = "DL Sprint 4.0"

SECONDS_BETWEEN_EMAILS = 0.5

# Competition links
KAGGLE_LINK_1 = "https://www.kaggle.com/t/be8384727a28293dd012ee3ce5df9bac"
KAGGLE_LINK_2 = "https://www.kaggle.com/t/fbf7ab57b50a41c59aae973a725b9a4f"
RULEBOOK_LINK = "https://tinyurl.com/DLSprint4Rulebook"

TEST_TEAM_NAME = "Team_Test for Organizers"

SUBJECT = " DL Sprint 4.0 Online Round is Live!! | BUET CSE Fest 2026"

EMAIL_BODY = """\
<html>
<body>
<p>Dear Team <strong>{team_name}</strong>,</p>

<p>Greetings from BUET CSE Fest 2026!</p>

<p>We are thrilled to announce that the <strong>DL Sprint 4.0 Online Round</strong> has officially started! </p>

<p>📅 <strong>Competition Duration:</strong> 22 Days</p>

<p>🔗 <strong>Kaggle Competition Links:</strong></p>
<ul>
  <li>Competition 1: <a href="{kaggle_link_1}">{kaggle_link_1}</a></li>
  <li>Competition 2: <a href="{kaggle_link_2}">{kaggle_link_2}</a></li>
</ul>

<p>📖 <strong>Rulebook:</strong> <a href="{rulebook_link}">{rulebook_link}</a></p>

<p>Please make sure to:</p>
<ul>
  <li> Read the rulebook carefully before starting</li>
  <li> Join both Kaggle competitions using the links above</li>
  <li> Submit your solutions before the deadline</li>
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


# ========================================
# HELPER FUNCTIONS
# ========================================

def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def load_sent_log():
    """Load the log of teams that have already been sent emails"""
    if os.path.exists(SENT_LOG_FILE):
        with open(SENT_LOG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"sent_teams": [], "last_updated": None}


def save_sent_log(sent_log):
    """Save the sent teams log"""
    sent_log["last_updated"] = now_iso()
    with open(SENT_LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(sent_log, f, indent=4, ensure_ascii=False)


def extract_teams_from_csv():
    """Extract team information from CSV"""
    if not os.path.exists(CSV_FILE):
        print(f"❌ ERROR: {CSV_FILE} not found")
        sys.exit(1)
    
    df = pd.read_csv(CSV_FILE)
    email_columns = [col for col in df.columns if 'Email' in col and col != 'Email address']
    
    teams = []
    for idx, row in df.iterrows():
        team_name = row['Team Name']
        emails = set()
        
        for col in email_columns:
            email = row[col]
            if pd.notna(email) and isinstance(email, str) and email.strip() and '@' in email:
                emails.add(email.strip())
        
        if emails:
            teams.append({
                "team_name": team_name,
                "emails": list(emails)
            })
    
    return teams


def get_new_teams(all_teams, sent_log):
    """Find teams that haven't been emailed yet"""
    sent_team_names = set(sent_log.get("sent_teams", []))
    return [t for t in all_teams if t["team_name"] not in sent_team_names]


def send_email_with_cc(to_email: str, cc_emails: list, team_name: str) -> tuple:
    """Send email via Brevo API with CC recipients"""
    if not BREVO_API_KEY:
        return False, "Missing BREVO_API_KEY"
    
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
            return True, r.json().get("messageId", "OK")
        else:
            return False, f"HTTP {r.status_code}: {r.text}"
    except Exception as e:
        return False, str(e)


# ========================================
# MAIN
# ========================================

def main():
    parser = argparse.ArgumentParser(description="Send DL Sprint emails to NEW teams only")
    parser.add_argument("--check", action="store_true", help="Just show new teams (dry run)")
    parser.add_argument("--test", action="store_true", help="Test mode: only send to test team")
    args = parser.parse_args()

    # Load current state
    sent_log = load_sent_log()
    all_teams = extract_teams_from_csv()
    new_teams = get_new_teams(all_teams, sent_log)

    # Status
    print(f"\n{'='*60}")
    print(f"📊 STATUS")
    print(f"{'='*60}")
    print(f"   Total teams in CSV: {len(all_teams)}")
    print(f"   Teams already emailed: {len(sent_log.get('sent_teams', []))}")
    print(f"   New teams to process: {len(new_teams)}")
    print(f"{'='*60}\n")

    if not new_teams:
        print("✅ No new teams to process!")
        return

    # List new teams
    print("📋 New Teams:")
    for i, team in enumerate(new_teams, 1):
        print(f"   {i}. {team['team_name']} ({len(team['emails'])} members)")
        for email in team['emails']:
            print(f"      - {email}")
    print()

    # If just checking, stop here
    if args.check:
        print("ℹ️  Dry run mode. No emails sent.")
        return

    # Test mode
    if args.test:
        new_teams = [t for t in new_teams if t['team_name'] == TEST_TEAM_NAME]
        if not new_teams:
            # Try from all teams for test
            new_teams = [t for t in all_teams if t['team_name'] == TEST_TEAM_NAME]
        if not new_teams:
            print(f"❌ Test team '{TEST_TEAM_NAME}' not found")
            return
        print(f"🧪 TEST MODE: Only sending to '{TEST_TEAM_NAME}'\n")
    else:
        # Confirmation for production
        if not BREVO_API_KEY:
            print("❌ ERROR: BREVO_API_KEY not set in environment")
            sys.exit(1)
        
        confirm = input(f"📧 Send emails to {len(new_teams)} new teams? Type 'yes' to confirm: ")
        if confirm.lower() != 'yes':
            print("Aborted.")
            return

    # Send emails
    print(f"\n{'='*60}")
    print(f"📤 SENDING EMAILS")
    print(f"{'='*60}")
    print(f"Started at: {now_iso()}\n")

    success_count = 0
    fail_count = 0
    successfully_sent_teams = []

    for i, team in enumerate(new_teams, 1):
        team_name = team['team_name']
        emails = team['emails']

        if not emails:
            print(f"[{i}/{len(new_teams)}] ⚠️  {team_name}: No emails, skipping")
            continue

        to_email = emails[0]
        cc_emails = emails[1:] if len(emails) > 1 else []

        print(f"[{i}/{len(new_teams)}] 📤 {team_name}")
        print(f"    TO: {to_email}")
        if cc_emails:
            print(f"    CC: {', '.join(cc_emails)}")

        success, info = send_email_with_cc(to_email, cc_emails, team_name)

        if success:
            print(f"    ✅ Sent (ID: {info})")
            success_count += 1
            successfully_sent_teams.append(team_name)
        else:
            print(f"    ❌ Failed: {info}")
            fail_count += 1

        if i < len(new_teams):
            time.sleep(SECONDS_BETWEEN_EMAILS)

    # Update sent log with successfully sent teams
    if successfully_sent_teams:
        for team_name in successfully_sent_teams:
            if team_name not in sent_log["sent_teams"]:
                sent_log["sent_teams"].append(team_name)
        save_sent_log(sent_log)
        print(f"\n✅ Updated {SENT_LOG_FILE} with {len(successfully_sent_teams)} new teams")

    # Summary
    print(f"\n{'='*60}")
    print(f"📊 SUMMARY")
    print(f"{'='*60}")
    print(f"   ✅ Successful: {success_count}")
    print(f"   ❌ Failed: {fail_count}")
    print(f"   📁 Tracking updated: {SENT_LOG_FILE}")
    print(f"   Finished at: {now_iso()}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()

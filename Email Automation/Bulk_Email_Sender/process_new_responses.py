#!/usr/bin/env python3
"""
Process New Responses - Handles incremental Google Form responses
Tracks which teams have been emailed and only processes new ones.

Usage:
    python process_new_responses.py --check      # Just show new teams (dry run)
    python process_new_responses.py --generate   # Generate JSON for new teams only
    python process_new_responses.py --mark-sent  # Mark teams as sent after emailing
"""

import pandas as pd
import json
import os
import argparse
from datetime import datetime

# Configuration
CSV_FILE = "DL Sprint Team Registration Form (Responses) - Form responses 1_new.csv"  # Always use latest
SENT_LOG_FILE = "sent_teams.json"  # Tracks which teams have been emailed
NEW_TEAMS_JSON = "new_team_emails.json"  # Output for new teams only
ALL_TEAMS_JSON = "team_emails.json"  # Full list


def load_sent_log():
    """Load the log of teams that have already been sent emails"""
    if os.path.exists(SENT_LOG_FILE):
        with open(SENT_LOG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"sent_teams": [], "last_updated": None}


def save_sent_log(sent_log):
    """Save the sent teams log"""
    sent_log["last_updated"] = datetime.now().isoformat()
    with open(SENT_LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(sent_log, f, indent=4, ensure_ascii=False)
    print(f"✓ Updated {SENT_LOG_FILE}")


def extract_teams_from_csv(csv_file):
    """Extract team information from CSV"""
    df = pd.read_csv(csv_file)
    email_columns = [col for col in df.columns if 'Email' in col and col != 'Email address']
    
    teams = []
    for idx, row in df.iterrows():
        team_name = row['Team Name']
        timestamp = row.get('Timestamp', '')
        emails = set()
        
        for col in email_columns:
            email = row[col]
            if pd.notna(email) and isinstance(email, str) and email.strip() and '@' in email:
                emails.add(email.strip())
        
        if emails:
            teams.append({
                "team_name": team_name,
                "emails": list(emails),
                "timestamp": timestamp
            })
    
    return teams


def get_new_teams(all_teams, sent_log):
    """Find teams that haven't been emailed yet"""
    sent_team_names = set(sent_log.get("sent_teams", []))
    new_teams = [t for t in all_teams if t["team_name"] not in sent_team_names]
    return new_teams


def main():
    parser = argparse.ArgumentParser(description="Process new form responses")
    parser.add_argument('--check', action='store_true', help='Show new teams (dry run)')
    parser.add_argument('--generate', action='store_true', help='Generate JSON for new teams')
    parser.add_argument('--mark-sent', action='store_true', help='Mark new teams as sent')
    parser.add_argument('--mark-all', action='store_true', help='Mark ALL current teams as sent (initial setup)')
    args = parser.parse_args()

    # Load current state
    sent_log = load_sent_log()
    all_teams = extract_teams_from_csv(CSV_FILE)
    
    print(f"\n📊 Status:")
    print(f"   Total teams in CSV: {len(all_teams)}")
    print(f"   Teams already emailed: {len(sent_log.get('sent_teams', []))}")
    
    if args.mark_all:
        # Mark all current teams as sent (use this for initial setup)
        sent_log["sent_teams"] = [t["team_name"] for t in all_teams]
        save_sent_log(sent_log)
        print(f"\n✓ Marked all {len(all_teams)} teams as sent")
        return
    
    new_teams = get_new_teams(all_teams, sent_log)
    print(f"   New teams to process: {len(new_teams)}")
    
    if not new_teams:
        print("\n✓ No new teams to process!")
        return
    
    print(f"\n📋 New Teams:")
    for i, team in enumerate(new_teams, 1):
        print(f"   {i}. {team['team_name']} ({len(team['emails'])} members)")
        if args.check:
            for email in team['emails']:
                print(f"      - {email}")
    
    if args.generate:
        # Generate JSON file for new teams only
        output_teams = [{"team_name": t["team_name"], "emails": t["emails"]} for t in new_teams]
        with open(NEW_TEAMS_JSON, 'w', encoding='utf-8') as f:
            json.dump(output_teams, f, indent=4, ensure_ascii=False)
        print(f"\n✓ Generated {NEW_TEAMS_JSON} with {len(new_teams)} new teams")
        print(f"   Total emails: {sum(len(t['emails']) for t in new_teams)}")
    
    if args.mark_sent:
        # Mark new teams as sent
        for team in new_teams:
            if team["team_name"] not in sent_log["sent_teams"]:
                sent_log["sent_teams"].append(team["team_name"])
        save_sent_log(sent_log)
        print(f"\n✓ Marked {len(new_teams)} new teams as sent")


if __name__ == "__main__":
    main()

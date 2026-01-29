import pandas as pd
import json
import re

# Read the CSV file
csv_file = "DL Sprint Team Registration Form (Responses) - Form responses 1.csv"
df = pd.read_csv(csv_file)

# Get only member email columns (exclude "Email address" which is form submission email)
email_columns = [col for col in df.columns if 'Email' in col and col != 'Email address']

# Build list of team entries (to handle duplicate team names)
team_emails_list = []

for idx, row in df.iterrows():
    team_name = row['Team Name']
    emails = set()  # Use set to avoid duplicates
    
    for col in email_columns:
        email = row[col]
        # Check if email is non-empty and valid
        if pd.notna(email) and isinstance(email, str) and email.strip():
            # Basic email validation
            if '@' in email:
                emails.add(email.strip())
    
    if emails:
        email_list = list(emails)
        team_emails_list.append({
            "team_name": team_name,
            "emails": email_list
        })
        
        # Validation: warn if more than 4 members
        if len(email_list) > 4:
            print(f"WARNING: {team_name} has {len(email_list)} emails (expected max 4)")

# Save to JSON file
output_file = "team_emails.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(team_emails_list, f, indent=4, ensure_ascii=False)

print(f"\nGenerated {output_file} with {len(team_emails_list)} teams")
print(f"Total emails extracted: {sum(len(t['emails']) for t in team_emails_list)}")

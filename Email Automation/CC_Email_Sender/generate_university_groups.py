#!/usr/bin/env python3
"""
Generate university_teams.json from BUET IUPC registration CSV
Run this script whenever the CSV is updated with new responses
"""

import pandas as pd
import json
import re
from collections import defaultdict
from pathlib import Path

def normalize_university_name(name):
    """Normalize university name for grouping"""
    if pd.isna(name):
        return None
    
    # Convert to string and lowercase
    normalized = str(name).lower()
    
    # Strip leading and trailing spaces first
    normalized = normalized.strip()
    
    # Remove content in parentheses (like "MIST", "UITS", etc.)
    normalized = re.sub(r'\s*\([^)]*\)', '', normalized)
    
    # Replace multiple spaces with single space
    normalized = re.sub(r'\s+', ' ', normalized)
    
    # Normalize & and "and"
    normalized = normalized.replace(' & ', ' and ')
    normalized = normalized.replace('&', ' and ')
    
    # Fix common typos
    typo_map = {
        'bangaldesh': 'bangladesh',
        'engineerign': 'engineering',
        'gopalgonj': 'gopalganj',
    }
    
    for typo, correct in typo_map.items():
        normalized = normalized.replace(typo, correct)
    
    # Remove trailing punctuation
    normalized = normalized.rstrip('.')
    
    # Final trim
    normalized = normalized.strip()
    
    return normalized

def generate_university_groups():
    # File paths
    csv_file = 'BUET IUPC 2026 – Preliminary  Registration (Responses) - Form responses 1.csv'
    output_json = 'university_teams.json'
    output_csv = 'university_groups.csv'
    
    # Check if CSV exists
    if not Path(csv_file).exists():
        print(f"Error: {csv_file} not found!")
        return
    
    # Read the CSV file
    print(f"Reading {csv_file}...")
    df = pd.read_csv(csv_file)
    
    # Column names
    university_col = 'Full Name of the University (Or IOI)'
    team_col = 'Team Name'
    coach_email_col = 'Coach Email'
    
    # Create a dictionary grouped by university
    # Keep track of original university names for display
    university_groups = defaultdict(lambda: {
        'teams': [],
        'coach_emails': set(),
        'original_name': None
    })
    
    # Process each row
    for _, row in df.iterrows():
        university = row[university_col]
        team = row[team_col]
        coach_email = row[coach_email_col]
        
        if pd.notna(university) and pd.notna(coach_email):
            # Normalize for grouping
            normalized_uni = normalize_university_name(university)
            if normalized_uni:
                # Keep the first occurrence's original name for display
                if university_groups[normalized_uni]['original_name'] is None:
                    university_groups[normalized_uni]['original_name'] = str(university).strip()
                
                university_groups[normalized_uni]['teams'].append({
                    'team_name': team,
                    'coach_email': coach_email
                })
                university_groups[normalized_uni]['coach_emails'].add(coach_email)
    
    # Convert to list format for JSON
    result = []
    for normalized_uni, data in sorted(university_groups.items(), key=lambda x: x[1]['original_name']):
        result.append({
            'university': data['original_name'],
            'coach_emails': sorted(list(data['coach_emails'])),
            'team_count': len(data['teams']),
            'teams': data['teams']
        })
    
    # Save as JSON
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Created {output_json}")
    print(f"  - {len(result)} universities")
    print(f"  - {sum(len(u['teams']) for u in result)} total teams")
    
    # Create a CSV format for easy CC list
    csv_data = []
    for uni_data in result:
        csv_data.append({
            'University': uni_data['university'],
            'Team Count': uni_data['team_count'],
            'Coach Emails (CC)': '; '.join(uni_data['coach_emails']),
            'Teams': '; '.join([t['team_name'] for t in uni_data['teams']])
        })
    
    csv_df = pd.DataFrame(csv_data)
    csv_df.to_csv(output_csv, index=False, encoding='utf-8')
    
    print(f"✓ Created {output_csv} (for easy viewing)")
    
    # Show sample
    print(f"\nSample entry:")
    print(json.dumps(result[0], indent=2))
    
    return result

if __name__ == '__main__':
    generate_university_groups()

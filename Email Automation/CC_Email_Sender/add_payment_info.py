#!/usr/bin/env python3
"""Add payment information (Bkash number and account holder name) to university_teams.json.

Reads Final_Slot_With_Bkash.csv and merges payment details into the JSON file.
"""
import argparse
import csv
import json
import os
import sys


def normalize_university_name(name):
    """Normalize university name for comparison."""
    return name.strip().upper()


def load_payment_info(csv_file, encoding='utf-8-sig'):
    """Load payment info from CSV into a dictionary keyed by university name."""
    payment_map = {}
    with open(csv_file, newline='', encoding=encoding) as f:
        reader = csv.DictReader(f)
        for row in reader:
            uni = row.get('University Name', '').strip()
            bkash = row.get('Bkash', '').strip()
            name = row.get('Name', '').strip()
            if uni:
                key = normalize_university_name(uni)
                payment_map[key] = {
                    'bkash_account': bkash,
                    'account_holder_name': name
                }
    return payment_map


def add_payment_info(json_file, payment_map, output_file=None, encoding='utf-8'):
    """Add payment info to each university in JSON."""
    with open(json_file, 'r', encoding=encoding) as f:
        data = json.load(f)
    
    matched = 0
    unmatched = []
    
    for entry in data:
        uni = entry.get('university', '')
        key = normalize_university_name(uni)
        if key in payment_map:
            entry['payment_info'] = payment_map[key]
            matched += 1
        else:
            unmatched.append(uni)
    
    target = output_file if output_file else json_file
    with open(target, 'w', encoding=encoding) as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f'✓ Processed {len(data)} universities')
    print(f'✓ Matched {matched} with payment info')
    if unmatched:
        print(f'⚠ {len(unmatched)} universities without payment info:')
        for u in unmatched[:10]:
            print(f'  - {u}')
        if len(unmatched) > 10:
            print(f'  ... and {len(unmatched) - 10} more')
    print(f'✓ Updated JSON written to: {target}')
    
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description='Add payment info to university_teams.json')
    p.add_argument('--csv', default='Final_Slot_With_Bkash.csv', help='CSV file with payment info')
    p.add_argument('--json', default='university_teams.json', help='JSON file to update')
    p.add_argument('-o', '--out', help='Output JSON file (default: overwrite input)')
    p.add_argument('--csv-encoding', default='utf-8-sig', help='CSV encoding')
    p.add_argument('--json-encoding', default='utf-8', help='JSON encoding')
    args = p.parse_args(argv)
    
    if not os.path.isfile(args.csv):
        print(f'Error: CSV file not found: {args.csv}')
        return 1
    if not os.path.isfile(args.json):
        print(f'Error: JSON file not found: {args.json}')
        return 2
    
    payment_map = load_payment_info(args.csv, encoding=args.csv_encoding)
    print(f'✓ Loaded payment info for {len(payment_map)} universities from CSV')
    
    return add_payment_info(args.json, payment_map, output_file=args.out, encoding=args.json_encoding)


if __name__ == '__main__':
    sys.exit(main())

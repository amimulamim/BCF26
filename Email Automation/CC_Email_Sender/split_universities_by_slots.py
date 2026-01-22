#!/usr/bin/env python3
"""Split university_teams.json into two files:
1. With payment info (allocated_slots > 0)
2. Without payment info (allocated_slots == 0)
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
                payment_info = {'bkash_account': bkash}
                if name:  # Only add name if not empty
                    payment_info['account_holder_name'] = name
                payment_map[key] = payment_info
    return payment_map


def split_and_add_payment(json_file, payment_map, 
                         with_slots_file='university_teams_with_payment.json',
                         zero_slots_file='university_teams_zero_slots.json',
                         encoding='utf-8'):
    """Split JSON by allocated_slots and add payment info where needed."""
    with open(json_file, 'r', encoding=encoding) as f:
        data = json.load(f)
    
    with_payment = []
    zero_slots = []
    
    matched = 0
    unmatched = []
    
    for entry in data:
        uni = entry.get('university', '')
        slots = entry.get('allocated_slots', 0)
        
        if slots > 0:
            # Add payment info for universities with slots
            key = normalize_university_name(uni)
            if key in payment_map:
                entry['payment_info'] = payment_map[key]
                matched += 1
            else:
                unmatched.append(uni)
            with_payment.append(entry)
        else:
            # No payment info needed for zero slots
            # Remove payment_info if it exists
            entry.pop('payment_info', None)
            zero_slots.append(entry)
    
    # Write both files
    with open(with_slots_file, 'w', encoding=encoding) as f:
        json.dump(with_payment, f, indent=2, ensure_ascii=False)
    
    with open(zero_slots_file, 'w', encoding=encoding) as f:
        json.dump(zero_slots, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print(f'\n✓ Split complete!')
    print(f'  • Total universities: {len(data)}')
    print(f'  • With allocated slots (>0): {len(with_payment)} → {with_slots_file}')
    print(f'  • With zero slots: {len(zero_slots)} → {zero_slots_file}')
    print(f'\n✓ Payment info added to {matched}/{len(with_payment)} universities with slots')
    
    if unmatched:
        print(f'\n⚠ {len(unmatched)} universities with slots but no payment info:')
        for u in unmatched[:10]:
            print(f'  - {u}')
        if len(unmatched) > 10:
            print(f'  ... and {len(unmatched) - 10} more')
    
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description='Split university JSON by allocated slots and add payment info')
    p.add_argument('--csv', default='Final_Slot_With_Bkash.csv', help='CSV file with payment info')
    p.add_argument('--json', default='university_teams.json', help='JSON file to split')
    p.add_argument('--with-payment', default='university_teams_with_payment.json', 
                   help='Output file for universities with payment info')
    p.add_argument('--zero-slots', default='university_teams_zero_slots.json',
                   help='Output file for universities with zero slots')
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
    
    return split_and_add_payment(args.json, payment_map, 
                                args.with_payment, args.zero_slots,
                                encoding=args.json_encoding)


if __name__ == '__main__':
    sys.exit(main())

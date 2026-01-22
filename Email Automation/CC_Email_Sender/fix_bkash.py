#!/usr/bin/env python3
"""Normalize Bkash numbers in a CSV.

Finds a column whose header contains 'bkash' (case-insensitive) and ensures
numbers that are 10 digits become 11 digits by prepending a leading '0'.
Writes to a new file by default, or overwrites in place with `--inplace`.
"""
import argparse
import csv
import os
import re
import sys


def normalize_bkash(value):
    if value is None:
        return ""
    s = str(value).strip()
    if s == "":
        return s
    digits = re.sub(r'\D', '', s)
    if digits == "":
        return s
    if len(digits) == 10:
        return '0' + digits
    # keep 11-digit values as-is; leave other lengths unchanged but return digits
    if len(digits) == 11:
        return digits
    return digits


def find_bkash_index(headers):
    for i, h in enumerate(headers):
        if h and 'bkash' in h.lower():
            return i
    return None


def process(infile, outfile, inplace=False, encoding='utf-8-sig'):
    with open(infile, newline='', encoding=encoding) as inf:
        reader = csv.reader(inf)
        rows = list(reader)
    if not rows:
        print('Input CSV is empty')
        return 1
    headers = rows[0]
    idx = find_bkash_index(headers)
    if idx is None:
        print("No column containing 'bkash' found in headers:", headers)
        return 2

    changed = 0
    total = 0
    for r in rows[1:]:
        total += 1
        # ensure row has enough columns
        if idx >= len(r):
            # extend row if needed
            r += [''] * (idx - len(r) + 1)
        old = r[idx]
        new = normalize_bkash(old)
        if new != old:
            r[idx] = new
            changed += 1

    target = infile if inplace else outfile
    # write
    tmp = target + '.tmp'
    with open(tmp, 'w', newline='', encoding=encoding) as outf:
        writer = csv.writer(outf)
        writer.writerows(rows)
    os.replace(tmp, target)

    print(f'Processed {infile}: total rows={total}, changed={changed}, written to {target}')
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description='Normalize Bkash numbers in CSV')
    p.add_argument('input', nargs='?', default='Final_Slot_With_Bkash.csv', help='Input CSV file')
    p.add_argument('-o', '--out', default='Final_Slot_With_Bkash_fixed.csv', help='Output CSV file (ignored if --inplace)')
    p.add_argument('--inplace', action='store_true', help='Replace the input file with the fixed file')
    p.add_argument('--encoding', default='utf-8-sig', help='File encoding to use')
    args = p.parse_args(argv)

    infile = args.input
    outfile = args.out
    if not os.path.isfile(infile):
        print('Input file not found:', infile)
        return 3
    return process(infile, outfile, inplace=args.inplace, encoding=args.encoding)


if __name__ == '__main__':
    sys.exit(main())

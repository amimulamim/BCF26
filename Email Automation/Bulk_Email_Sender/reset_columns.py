import pandas as pd
import os
import sys

# Path to the CSV file (from command line or default)
csv_file = sys.argv[1] if len(sys.argv) > 1 else 'form_response.csv'

# Check if file exists
if os.path.exists(csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Ensure "Send Now" column exists, if not add it
    if "Send Now" not in df.columns:
        df["Send Now"] = "YES"
    else:
        # If exists, set all values to "YES"
        df["Send Now"] = "YES"
    
    # Ensure "Mail Sent" column exists, if not add it
    if "Mail Sent" not in df.columns:
        df["Mail Sent"] = ""
    else:
        # If exists, clear all values (set to empty string)
        df["Mail Sent"] = ""
    
    # Write back to the CSV file
    df.to_csv(csv_file, index=False)
    print(f"✓ Successfully reset columns in {csv_file}")
    print(f"  - 'Send Now' column set to 'YES'")
    print(f"  - 'Mail Sent' column cleared (set to empty)")
else:
    print(f"✗ File '{csv_file}' not found!")

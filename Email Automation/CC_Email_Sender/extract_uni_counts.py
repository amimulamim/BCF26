import json
import csv
from pathlib import Path

ROOT = Path(__file__).parent
json_path = ROOT / "university_teams.json"
out_path = ROOT / "uni_team_counts.csv"

with json_path.open('r', encoding='utf-8') as f:
    data = json.load(f)

with out_path.open('w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['University', 'Team Count'])
    for item in data:
        writer.writerow([item.get('university', '').strip(), item.get('team_count', 0)])

print(f"Wrote {out_path}")

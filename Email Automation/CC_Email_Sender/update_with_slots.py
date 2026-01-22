import json
import csv

# Read final_slot.csv and create a dictionary
slots_dict = {}
with open('final_slot.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) == 2:
            university = row[0].strip()
            slots = int(row[1].strip())
            slots_dict[university] = slots

# Read university_teams.json
with open('university_teams.json', 'r', encoding='utf-8') as f:
    university_data = json.load(f)

# Add allocated_slots field to each university
for uni in university_data:
    uni_name = uni['university']
    uni['allocated_slots'] = slots_dict.get(uni_name, 0)

# Write updated JSON back
with open('university_teams.json', 'w', encoding='utf-8') as f:
    json.dump(university_data, f, indent=2, ensure_ascii=False)

# Create new CSV with university, teams (applied), and allocated slots
with open('university_summary.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['University', 'Teams (Applied)', 'Allocated Slots'])
    
    for uni in university_data:
        writer.writerow([
            uni['university'],
            uni['team_count'],
            uni['allocated_slots']
        ])

print("✓ Updated university_teams.json with allocated_slots field")
print("✓ Created university_summary.csv with university, teams (applied), and allocated slots")

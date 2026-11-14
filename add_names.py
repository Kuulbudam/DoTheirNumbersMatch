import csv

NAMES = {
    "N01": "Below the Target",
    "N02a": "The Q4 Print",
    "N02b": "The Annual Print",
    "N03": "Just Fourteen",
    "N04": "The New Method",
    "N07": "Seven Point Four",
    "N08": "The Net Figure",
    "N17": "The Gross Figure",
    "N19": "The December Print",
    "N21": "Six Point Five One",
    "N22": "The Seven Seventy-Two",
    "N33": "Which November",
}

rows = list(csv.DictReader(open("claims_final.csv", encoding="utf-8")))
fields = list(rows[0].keys())
if "case_name" not in fields:
    fields.insert(2, "case_name")  # right after sample

for r in rows:
    r["case_name"] = NAMES.get(r["id"], "")

with open("claims_final.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)

print(f"Added case_name to {len(rows)} rows")
for r in rows:
    print(f"  {r['id']}: {r['case_name']}")

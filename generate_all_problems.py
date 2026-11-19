import json
import sys
import os

from data_generators.problems_01_08 import problems as p_01_08
from data_generators.problems_50_69 import problems as p_50_69
from data_generators.problems_70_85 import problems as p_70_85
from data_generators.problems_86_100 import problems as p_86_100

all_problems = p_01_08 + p_50_69 + p_70_85 + p_86_100

print(f"Total problems collected: {len(all_problems)}")

# Check duplicates and missing
id_set = set()
for p in all_problems:
    pid = p['id']
    if pid in id_set:
        raise ValueError(f"Duplicate problem ID: {pid}")
    id_set.add(pid)

# Verify all 51 problems from 50 to 100 exist
missing_50_100 = []
for i in range(50, 101):
    pid = f"DRAGON-{i}"
    if pid not in id_set:
        missing_50_100.append(pid)

if missing_50_100:
    raise ValueError(f"Missing problems from 50 to 100: {missing_50_100}")

print("Validation: All 51 problems from 50 to 100 are present!")

# Verify test case counts and required fields
for p in all_problems:
    assert len(p.get('test_cases', [])) == 5, f"{p['id']} does not have exactly 5 test cases!"
    for field in ['title', 'chapter', 'description', 'python_starter', 'c_starter', 'solution_python', 'solution_c', 'editorial']:
        assert p.get(field), f"{p['id']} missing field: {field}"

# Write to data/problems.json
os.makedirs('data', exist_ok=True)
output_path = 'data/problems.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump({"problems": all_problems}, f, ensure_ascii=False, indent=2)

print(f"Successfully saved {len(all_problems)} problems to {output_path}!")

# Update database
from models.database import init_db, seed_problems_from_json, get_all_problems
init_db()
seed_problems_from_json()
db_problems = get_all_problems()
print(f"Database now contains {len(db_problems)} problems in total!")

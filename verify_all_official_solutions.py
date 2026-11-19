import json
from judge.engine import judge_submission

with open('data/problems.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    problems = data['problems']

print(f"Testing official Python solutions for all {len(problems)} problems...")

failed = []
passed = 0

for p in problems:
    pid = p['id']
    code = p['solution_python']
    test_cases = p['test_cases']
    
    result = judge_submission(code, 'python', test_cases)
    passed_count = result['passed_count']
    total = result['total_count']
    score = result['score']
    
    if passed_count != total or score != 100:
        print(f"FAILED: {pid} - {p['title']}: {passed_count}/{total} passed (Score: {score})")
        for r in result['test_results']:
            if r['verdict'] != 'AC':
                print(f"  Test {r['test_index']} status: {r['verdict']}")
                print(f"    Expected: {repr(r['expected_preview'])}")
                print(f"    Actual:   {repr(r['actual_preview'])}")
                if r['error_detail']:
                    print(f"    Error:    {r['error_detail']}")
        failed.append(pid)
    else:
        passed += 1

print("=" * 60)
print(f"SUMMARY: {passed}/{len(problems)} passed with 100/100 AC!")
if failed:
    print(f"Failed problem IDs: {failed}")
else:
    print("ALL 59 PROBLEMS PASSED 100% PERFECTLY!")

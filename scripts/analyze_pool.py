#!/usr/bin/env python3

import json
from collections import Counter
from pathlib import Path

def count_questions_by_group(pool_file: str) -> tuple[dict, dict]:
    """Count how many questions are in each group of the question pool."""
    with open(pool_file) as f:
        data = json.load(f)
    
    # Count questions per group
    group_counts = Counter(q["group"] for q in data["questions"])
    
    # Sort by group ID and return with group titles
    return dict(sorted(group_counts.items())), data["group_titles"]

def main():
    pool_file = "data/technician-2022-2026.json"
    counts, group_titles = count_questions_by_group(pool_file)
    
    print(f"\nQuestion counts by group in {Path(pool_file).stem}:")
    print("-" * 40)
    for group, count in counts.items():
        print(f"{group}: {count} questions")
        
if __name__ == "__main__":
    main()

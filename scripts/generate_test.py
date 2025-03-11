#!/usr/bin/env python3

import json
import random
import argparse
from pathlib import Path
from datetime import datetime

def load_question_pool(json_file):
    """Load and parse the question pool JSON file."""
    with open(json_file, 'r') as f:
        return json.load(f)

def group_questions(questions):
    """Group questions by their group ID (e.g., T1A, T1B)."""
    grouped = {}
    for question in questions:
        group = question['group']
        if group not in grouped:
            grouped[group] = []
        grouped[group].append(question)
    return grouped

def generate_test(grouped_questions):
    """Generate a test by selecting one random question from each group."""
    test_questions = []
    for group, questions in sorted(grouped_questions.items()):
        selected = random.choice(questions)
        test_questions.append(selected)
    return test_questions

def save_test(test_questions, pool_data, output_dir):
    """Save the generated test to a JSON file."""
    # Create output directory if it doesn't exist
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate unique test ID using timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_id = f"test_{timestamp}"
    
    test_data = {
        "test_id": test_id,
        "timestamp": datetime.now().isoformat(),
        "source_pool": {
            "license_class": pool_data["license_class"],
            "version": pool_data["version"],
            "file": str(Path(pool_data["_source_file"]).name)
        },
        "questions": test_questions
    }
    
    # Include license class and version in filename
    filename = f"{pool_data['license_class']}-{pool_data['version']}-{test_id}.json"
    output_file = output_dir / filename
    with open(output_file, 'w') as f:
        json.dump(test_data, f, indent=2)
    
    return output_file

def main():
    parser = argparse.ArgumentParser(description='Generate a randomized amateur radio test')
    parser.add_argument('--pool-file', required=True,
                      help='Path to the JSON question pool file')
    parser.add_argument('--output-dir', default='data/tests',
                      help='Directory to save the generated test (default: data/tests)')
    args = parser.parse_args()
    
    pool_file = Path(args.pool_file)
    if not pool_file.exists():
        raise FileNotFoundError(f"Question pool file not found: {pool_file}")
    
    # Load and process questions
    pool_data = load_question_pool(pool_file)
    # Add source file information to pool data
    pool_data["_source_file"] = str(pool_file)
    
    grouped = group_questions(pool_data['questions'])
    test_questions = generate_test(grouped)
    
    # Save the test
    output_file = save_test(test_questions, pool_data, args.output_dir)
    print(f"Test generated and saved to: {output_file}")

if __name__ == '__main__':
    main() 

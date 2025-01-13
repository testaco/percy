#!/usr/bin/env python3

import json
import re
from docx import Document
from pathlib import Path
import argparse

def extract_question_pool(docx_path, debug=False):
    """Extract questions from the DOCX file and return structured data."""
    doc = Document(docx_path)
    questions = []
    current_question = None
    current_group = None
    in_question_pool = False
    expecting_question_text = False
    
    # Regular expressions for parsing
    question_id_pattern = re.compile(r'^([TG|E]\d[A-Z])\d{2}\s*\(([A-D])\)')
    answer_pattern = re.compile(r'^([A-D])\.\s*(.+)$')
    section_pattern = re.compile(r'^[TG|E]\d[A-D]\s*[-–]\s*.*$')
    
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
            
        if debug:
            print(f"Processing text: {text}")
            print(f"Style: {para.style.name}")
            
        # Skip until we find the start of the question pool
        if "SUBELEMENT" in text:
            in_question_pool = True
            continue
            
        if not in_question_pool:
            continue
            
        # Skip section headers
        if section_pattern.match(text):
            continue
            
        # Check if this is a new question
        match = question_id_pattern.match(text)
        if match:
            if current_question and len(current_question["answers"]) > 0:
                if debug:
                    print(f"Adding question: {json.dumps(current_question, indent=2)}")
                questions.append(current_question)
            
            # Extract question components
            group = match.group(1)
            correct_answer = match.group(2)
            question_id = text.split('(')[0].strip()
            
            current_question = {
                "id": question_id,
                "group": group,
                "question": "",
                "answers": [],
                "correct_answer": correct_answer
            }
            
            expecting_question_text = True
            
            if debug:
                print(f"New question: {question_id}")
                print(f"Group: {group}")
                print(f"Correct answer: {correct_answer}")
        
        # Check if this is the question text (comes after the question ID)
        elif expecting_question_text and not answer_pattern.match(text):
            # Remove reference numbers in square brackets
            question_text = re.sub(r'\[.*?\]', '', text).strip()
            current_question["question"] = question_text
            expecting_question_text = False
            
            if debug:
                print(f"Question text: {question_text}")
        
        # Check if this is an answer choice
        else:
            answer_match = answer_pattern.match(text)
            if current_question and answer_match:
                option = answer_match.group(1)
                answer_text = answer_match.group(2).strip()
                
                current_question["answers"].append({
                    "option": option,
                    "text": answer_text
                })
                
                if debug:
                    print(f"Added answer {option}: {answer_text}")
    
    # Add the last question
    if current_question and len(current_question["answers"]) > 0:
        if debug:
            print(f"Adding final question: {json.dumps(current_question, indent=2)}")
        questions.append(current_question)
    
    return questions

def test_first_question():
    """Test function to verify the first question matches expected format."""
    expected = {
        "id": "T1A01",
        "group": "T1A",
        "question": "Which of the following is part of the Basis and Purpose of the Amateur Radio Service?",
        "answers": [
            {"option": "A", "text": "Providing personal radio communications for as many citizens as possible"},
            {"option": "B", "text": "Providing communications for international non-profit organizations"},
            {"option": "C", "text": "Advancing skills in the technical and communication phases of the radio art"},
            {"option": "D", "text": "All these choices are correct"}
        ],
        "correct_answer": "C"
    }
    
    questions = extract_question_pool('data/technician-2022-2026.docx', debug=True)
    if not questions:
        print("Error: No questions extracted")
        return False
        
    first_question = questions[0]
    
    # Compare each field
    fields_match = all([
        first_question["id"] == expected["id"],
        first_question["group"] == expected["group"],
        first_question["question"] == expected["question"],
        first_question["correct_answer"] == expected["correct_answer"],
        len(first_question["answers"]) == len(expected["answers"])
    ])
    
    # Compare answers
    answers_match = all(
        a1["option"] == a2["option"] and a1["text"] == a2["text"]
        for a1, a2 in zip(first_question["answers"], expected["answers"])
    )
    
    if not fields_match or not answers_match:
        print("\nExpected:")
        print(json.dumps(expected, indent=2))
        print("\nGot:")
        print(json.dumps(first_question, indent=2))
        return False
        
    print("First question matches expected format!")
    return True

def main():
    parser = argparse.ArgumentParser(description='Convert Amateur Radio Question Pool from DOCX to JSON')
    parser.add_argument('--input', required=True,
                      help='Input DOCX file path')
    parser.add_argument('--output', required=True,
                      help='Output JSON file path')
    parser.add_argument('--test', action='store_true',
                      help='Run test to verify first question format')
    parser.add_argument('--debug', action='store_true',
                      help='Enable debug output')
    
    args = parser.parse_args()
    
    if args.test:
        success = test_first_question()
        if not success:
            print("Test failed!")
            return 1
        return 0
    
    # Create output directory if it doesn't exist
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Extract questions
    questions = extract_question_pool(args.input, debug=args.debug)
    
    # Write to JSON file
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump({
            "license_class": "technician",
            "version": "2022-2026",
            "questions": questions
        }, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully converted {len(questions)} questions to {args.output}")

if __name__ == "__main__":
    main() 
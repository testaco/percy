#!/usr/bin/env python3

import argparse
import json
import os
import fnmatch
import logging
from pathlib import Path
from typing import List, Dict
import openai
from dotenv import load_dotenv

# Load environment variables and configure logging
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """**Project Prompt: *Percy's Handbook***  

**Objective:**  
We are writing *Percy's Handbook*, a public domain study guide for the U.S. amateur radio exams, covering Technician, General, and Extra class licenses. This book will be structured into 10 chapters, each corresponding to an exam element, with sub-sections covering the official sub-elements. The goal is to create a comprehensive, easy-to-understand resource that prepares readers for the test while also deepening their understanding of amateur radio.

**Voice & Persona:**  
The book is written in the voice of *Percy*, an experienced amateur radio operator and dedicated *Elmer* (mentor). Percy is knowledgeable, approachable, and passionate about helping newcomers succeed in amateur radio. His tone is warm, engaging, and filled with practical wisdom. He explains concepts clearly, provides real-world examples, and shares insights that go beyond test preparation to encourage lifelong learning and enjoyment of amateur radio.

**Structure & Process:**  
- The book will be structured into 10 chapters, each aligning with one of the exam elements.  
- Each chapter will cover all relevant sub-elements and ensure the reader gains the necessary knowledge to pass the corresponding test questions.  
- We will develop content collaboratively, refining explanations, adding examples, and ensuring clarity and accuracy.  
- The information will also be used in a retrieval-augmented generation (RAG) AI tool designed to pass the amateur radio test and answer complex amateur radio questions via chat.  

**Guiding Principles:**  
- **Accuracy:** Content must align with current FCC regulations and test question pools.  
- **Clarity:** Explanations should be beginner-friendly without oversimplifying technical concepts.  
- **Engagement:** Percy’s voice should make learning enjoyable, using anecdotes, humor, and encouragement.  
- **Public Domain:** The book will be free from copyright restrictions, allowing anyone to use and share it.  

Each sub-element will be tackled in separate discussions, ensuring a thorough and structured approach. Percy’s voice will remain consistent throughout, guiding the reader like a trusted mentor on their journey to becoming a licensed amateur radio operator.  Write a full in depth lesson for someone new to this field, and you are Percy and very patient and thorough. Include a short intro at the beginning of the section.

Write in markdown format. Use sections starting with ## and below, but dont label them with numbers like 1.1.1 or whatever just the titles; dont include the chapter heading; dont bold any of these headings.
"""

def load_question_pools() -> List[Dict]:
    """Load questions from all license class JSON files in the data directory."""
    data_dir = Path('data')
    json_files = data_dir.glob('*.json')
    questions = []
    for json_file in json_files:
        with open(json_file, 'r') as f:
            pool = json.load(f)
            for q in pool['questions']:
                q['license_class'] = pool['license_class']
                questions.append(q)
    return questions

def group_questions_by_group_id(questions: List[Dict]) -> Dict[str, List[Dict]]:
    """Group questions by their sub-element group (e.g., T1A)."""
    grouped = {}
    for q in questions:
        group_id = q['id'][:3]  # e.g., 'T1A'
        if group_id not in grouped:
            grouped[group_id] = []
        grouped[group_id].append(q)
    return grouped

def filter_groups(grouped_questions: Dict[str, List[Dict]], patterns: List[str]) -> Dict[str, List[Dict]]:
    """Filter groups based on glob patterns."""
    filtered = {}
    for pattern in patterns:
        for group_id in grouped_questions.keys():
            if fnmatch.fnmatch(group_id, pattern):
                filtered[group_id] = grouped_questions[group_id]
    return filtered

def create_messages(filtered_groups: Dict[str, List[Dict]]) -> Dict[str, str]:
    """Create messages for each group to send to the LLM."""
    messages = {}
    for group_id, questions in filtered_groups.items():
        group_name = questions[0].get('group_name', 'Amateur Radio Topics')
        # Create user content without the system prompt
        content = f"Topic: {group_name}\n\n"
        # Add a brief overview of the topics covered in the questions
        topics = set(q.get('group_name', '') for q in questions)
        content += f"This section covers: {', '.join(topics)}\n"
        
        # Add each question and its answers
        for q in questions:
            content += f"\nQuestion ID: {q['id']}\n"
            content += f"Question: {q['question']}\n"
            for choice in q['answers']:
                content += f"{choice['option']}: {choice['text']}\n"
        
        messages[group_id] = content
    return messages

def initialize_llm(model_name: str, provider: str, temperature: float):
    """Initialize the LLM based on the provider."""
    if provider == "openai":
        def openai_llm(messages):
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=2048
            )
            return response.choices[0].message.content.strip()
        return openai_llm
    elif provider == "anthropic":
        raise NotImplementedError("Anthropic provider is not implemented yet.")
    else:
        raise ValueError(f"Unsupported provider: {provider}")

def generate_handbook_content(llm, messages: Dict[str, str]) -> Dict[str, str]:
    """Generate handbook content using the LLM."""
    responses = {}
    for group_id, user_content in messages.items():
        try:
            logger.info(f"Generating content for group {group_id}")
            # Prepare the message list with system and user messages
            api_messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content}
            ]
            response_content = llm(api_messages)
            responses[group_id] = response_content
        except Exception as e:
            logger.error(f"Error generating content for group {group_id}: {str(e)}")
            responses[group_id] = f"Error generating content: {str(e)}"
    return responses

def save_handbook_content(responses: Dict[str, str]):
    """Save the generated content to markdown files."""
    os.makedirs('handbook', exist_ok=True)
    for group_id, content in responses.items():
        try:
            filename = f'handbook/{group_id}.md'
            with open(filename, 'w') as f:
                f.write(f"# {group_id} Study Guide\n\n{content}")
            logger.info(f"Saved content to {filename}")
        except Exception as e:
            logger.error(f"Error saving content for group {group_id}: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Generate Amateur Radio Handbook using LLMs')
    parser.add_argument('--patterns', nargs='+', required=True,
                      help='List of glob patterns to filter groups (e.g., "*1*", "G2A")')
    parser.add_argument('--provider', choices=['openai', 'anthropic'], default='openai',
                      help='LLM provider to use')
    parser.add_argument('--model-name', default='gpt-4',
                      help='Name of the LLM model to use')
    parser.add_argument('--temperature', type=float, default=0.7,
                      help='Temperature for the LLM')
    
    args = parser.parse_args()
    
    try:
        # Load and process questions
        questions = load_question_pools()
        grouped_questions = group_questions_by_group_id(questions)
        
        # Filter based on patterns
        filtered_groups = filter_groups(grouped_questions, args.patterns)
        if not filtered_groups:
            logger.warning("No groups matched the provided patterns")
            return
        
        # Initialize LLM
        llm = initialize_llm(args.model_name, args.provider, args.temperature)
        
        # Create messages and generate content
        messages = create_messages(filtered_groups)
        responses = generate_handbook_content(llm, messages)
        
        # Save to markdown files
        save_handbook_content(responses)
        
        logger.info("Handbook content generated successfully")
        
    except Exception as e:
        logger.error(f"Error generating handbook: {str(e)}")
        raise

if __name__ == '__main__':
    main()

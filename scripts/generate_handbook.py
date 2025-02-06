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
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_system_prompt() -> str:
    """Load the system prompt from the prompts directory."""
    prompt_path = Path('handbook/prompts/group.md')
    if not prompt_path.exists():
        raise FileNotFoundError(f"System prompt file not found at {prompt_path}")
    return prompt_path.read_text()
SYSTEM_PROMPT = load_system_prompt()

def load_question_pools() -> List[Dict]:
    """Load questions from all license class JSON files in the data directory."""
    data_dir = Path('data')
    json_files = data_dir.glob('*.json')
    questions = []
    for json_file in json_files:
        with open(json_file, 'r') as f:
            pool = json.load(f)
            group_titles = pool.get('group_titles', {})
            for q in pool['questions']:
                q['license_class'] = pool['license_class']
                # Add the group title to each question
                q['group_title'] = group_titles.get(q['group'], '')
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
        # Get the group title from the first question's pool data
        group_title = questions[0].get('group_title', 'Amateur Radio Topics')
        
        # Create user content without the system prompt
        content = f"Group: {group_id} - {group_title}\n\n"
        
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
            # Debug log the full messages being sent
            logger.debug(f"Sending messages to LLM for {group_id}:")
            for msg in api_messages:
                logger.debug(f"Role: {msg['role']}")
                logger.debug(f"Content:\n{msg['content']}\n")
                
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
    parser.add_argument('--debug', action='store_true',
                      help='Enable debug logging')
    
    args = parser.parse_args()
    
    # Set debug logging if flag is set
    if args.debug:
        logger.setLevel(logging.DEBUG)
        # Also set OpenAI debug logging
        logging.getLogger("openai").setLevel(logging.DEBUG)
    
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

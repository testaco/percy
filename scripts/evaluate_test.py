#!/usr/bin/env python3
"""
Evaluate an LLM's performance on an amateur radio exam using litellm.
"""

import argparse
import base64
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from litellm import completion
from litellm.exceptions import APIError

from handbook_indexer import HandbookIndex
from dotenv import load_dotenv
from pydantic import BaseModel, Field, SecretStr
from PIL import Image

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)




class Answer(BaseModel):
    """Represents an answer choice."""
    option: str
    text: str

class Question(BaseModel):
    """Represents a single question from the test."""
    id: str
    group: str
    question: str
    answers: List[Answer]
    correct_answer: str
    has_image: bool = False
    image_path: Optional[str] = None

class TokenUsageDetails(BaseModel):
    """Details about token usage for specific features"""
    audio: int = 0
    cache_read: int = 0

class OutputTokenDetails(BaseModel):
    """Details about output token usage"""
    audio: int = 0
    reasoning: int = 0

class TokenUsage(BaseModel):
    """Complete token usage information"""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    input_token_details: TokenUsageDetails = Field(default_factory=TokenUsageDetails)
    output_token_details: OutputTokenDetails = Field(default_factory=OutputTokenDetails)

class TestResult(BaseModel):
    """Represents the results of a single test evaluation."""
    test_id: str
    model: str
    model_id: str
    organization_id: str
    provider_id: str
    timestamp: str
    questions: List[Dict]
    total_questions: int
    correct_answers: int
    score_percentage: float
    duration_seconds: float
    used_cot: bool
    used_rag: bool
    temperature: float
    token_usage: TokenUsage
    pool_name: str  # e.g. "technician", "general", "extra" 
    pool_id: str    # e.g. "technician-2022-2026"

def load_test(test_file: str) -> List[Question]:
    """Load test questions from a JSON file."""
    with open(test_file, 'r') as f:
        test_data = json.load(f)
    
    questions = []
    for q in test_data['questions']:
        # Check for figure references in the question text (both with and without hyphen)
        question_lower = q['question'].lower()
        
        # Check license class from test file name
        test_path = Path(test_file)
        is_general = "general" in test_path.stem.lower()
        is_extra = "extra" in test_path.stem.lower()
        
        # Handle Extra class figures
        if is_extra:
            # Page 1 figures (E5-1, E6-1, E6-2, E6-3)
            if any(x in question_lower for x in ["figure e5-1", "figure e5", "figure e-5", 
                                               "figure e6-1", "figure e-6-1",
                                               "figure e6-2", "figure e-6-2",
                                               "figure e6-3", "figure e-6-3"]):
                q['has_image'] = True
                q['image_path'] = "extra-2024-2028-diagrams-page1.jpg"
            # Page 2 figures (E7-1, E7-2, E7-3, E9-1)
            elif any(x in question_lower for x in ["figure e7-1", "figure e-7-1",
                                                 "figure e7-2", "figure e-7-2",
                                                 "figure e7-3", "figure e-7-3",
                                                 "figure e9-1", "figure e-9-1"]):
                q['has_image'] = True
                q['image_path'] = "extra-2024-2028-diagrams-page2.jpg"
            # Page 3 figures (E9-2, E9-3)
            elif any(x in question_lower for x in ["figure e9-2", "figure e-9-2",
                                                 "figure e9-3", "figure e-9-3"]):
                q['has_image'] = True
                q['image_path'] = "extra-2024-2028-diagrams-page3.jpg"
        # Handle General class figures
        elif is_general and any(x in question_lower for x in ["figure g7", "figure g-7", "figure g7-1", "figure g-7-1"]):
            q['has_image'] = True
            q['image_path'] = "G7-1.png"
        # Handle Technician class figures
        elif any(x in question_lower for x in ["figure t1", "figure t-1"]):
            q['has_image'] = True
            q['image_path'] = "T1.jpg"
        elif any(x in question_lower for x in ["figure t2", "figure t-2"]):
            q['has_image'] = True
            q['image_path'] = "T2.jpg"
        elif any(x in question_lower for x in ["figure t3", "figure t-3"]):
            q['has_image'] = True
            q['image_path'] = "T3.jpg"
        
        questions.append(Question(**q))
    return questions

def encode_image_to_base64(image_path: str) -> str:
    """Convert an image to base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def create_question_prompt(question: Question, use_cot: bool = False, rag_context: Optional[List[str]] = None) -> tuple[str, Dict]:
    """Create a prompt for the LLM based on the question."""
    # Convert answers list to choices dict
    choices = {answer.option: answer.text for answer in question.answers}
    
    base_prompt = """You are taking an amateur radio license exam. Please answer the following multiple choice question.
    {cot_instruction}
    {rag_context}
    Question: {question_text}

    Choices:
    A: {choice_a}
    B: {choice_b}
    C: {choice_c}
    D: {choice_d}

    {response_instruction}"""

    cot_instruction = """Think through this step-by-step, explaining your reasoning before giving your final answer.""" if use_cot else ""
    response_instruction = """Explain your reasoning step by step, then end with 'Therefore, my answer is: [A/B/C/D]'""" if use_cot else "Your answer (just the letter):"
    
    # Format RAG context if provided
    rag_text = ""
    if rag_context:
        rag_text = "Relevant context:\n" + "\n".join(f"- {ctx}" for ctx in rag_context) + "\n"
    
    if question.has_image and question.image_path:
        # Load and process the image
        image_path = os.path.join("data", question.image_path)
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        # Create base64 image data
        image_data = encode_image_to_base64(image_path)
        
        # Determine image content type from file extension
        image_type = "jpeg" if question.image_path.lower().endswith(".jpg") else "png"
        
        # Format the content as a list of text and image parts
        content = [
            {"type": "text", "text": base_prompt.format(
                cot_instruction=cot_instruction,
                rag_context=rag_text,
                question_text=question.question,
                choice_a=choices['A'],
                choice_b=choices['B'],
                choice_c=choices['C'],
                choice_d=choices['D'],
                response_instruction=response_instruction
            )},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/{image_type};base64,{image_data}"
                }
            }
        ]
        
        # Return a special format for image-based questions
        return "", {"content": content}
    else:
        return base_prompt, {
            "cot_instruction": cot_instruction,
            "rag_context": rag_text,
            "question_text": question.question,
            "choice_a": choices['A'],
            "choice_b": choices['B'],
            "choice_c": choices['C'],
            "choice_d": choices['D'],
            "response_instruction": response_instruction
        }

def extract_final_answer(response: str) -> str:
    """Extract the final answer letter from a Chain of Thought response.
    
    Args:
        response: The full response from the LLM
        
    Returns:
        A single letter (A, B, C, or D) representing the final answer
        
    Raises:
        ValueError: If no valid answer letter can be found
    """
    if not response:
        raise ValueError("No valid answer found in response")
    
    response = response.strip().upper()
    valid_answers = set(['A', 'B', 'C', 'D'])
    
    # First try to find "Therefore, my answer is: X" pattern
    if "THEREFORE, MY ANSWER IS:" in response:
        answer_part = response.split("THEREFORE, MY ANSWER IS:")[-1].strip()
        # Extract first valid letter after the pattern
        for char in answer_part:
            if char in valid_answers:
                return char
    
    # If not found, try the last line
    lines = response.split('\n')
    for line in reversed(lines):
        # Look for valid letters in the line
        for char in line:
            if char in valid_answers:
                return char
    
    # If still not found, look for "answer is X" pattern
    if "ANSWER IS" in response:
        answer_part = response.split("ANSWER IS")[-1].strip()
        for char in answer_part:
            if char in valid_answers:
                return char
    
    # Last resort: look for any valid letter in the last 50 characters
    # (avoiding picking up letters from the question/explanation)
    last_part = response[-50:]
    for char in reversed(last_part):
        if char in valid_answers:
            return char
    
    raise ValueError("No valid answer found in response")

def initialize_llm(model: str, temperature: float):
    """Initialize LiteLLM configuration"""
    # Validate model format
    if "/" not in model:
        raise ValueError("Model name must be in format 'provider/model'")
    return None  # No LLM object needed with LiteLLM's completion()

def get_pool_info(test_file: str) -> tuple[str, str]:
    """Extract pool name and ID from test file path."""
    file_name = Path(test_file).stem.lower()
    
    if "technician" in file_name:
        pool_name = "technician"
    elif "general" in file_name:
        pool_name = "general"
    elif "extra" in file_name:
        pool_name = "extra"
    else:
        pool_name = "unknown"
        
    # Extract full pool ID (e.g. technician-2022-2026)
    if any(year in file_name for year in ["2022-2026", "2023-2027", "2024-2028"]):
        pool_id = next(id for id in [
            "technician-2022-2026",
            "general-2023-2027",
            "extra-2024-2028"
        ] if id.split("-")[0] == pool_name)
    else:
        pool_id = f"{pool_name}-unknown"
        
    return pool_name, pool_id

def _normalize_ids(
  provider_id: str,
  organization_id: str,
  model_id: str
) -> tuple[str, str]:
  if provider_id == 'openrouter' and organization_id == 'google' and model_id == 'gemini-flash-1.5-8b':
    return 'google', 'gemini-1.5-flash-8b'
  raise NotImplementedError

def evaluate_test(
    test_file: str,
    model: str = "openai/gpt-3.5-turbo",
    temperature: float = 0.0,
    use_cot: bool = False,
    use_rag: bool = False
) -> TestResult:
    """Evaluate an LLM's performance on a test."""
    start_time = datetime.now()
    
    # Load the test
    questions = load_test(test_file)
    
    # Initialize token tracking
    total_prompt_tokens = 0
    total_completion_tokens = 0
    total_tokens = 0
    
    # Initialize RAG if enabled
    handbook_index = None
    if use_rag:
        handbook_index = HandbookIndex()
        handbook_index.build("handbook")
    
    # Initialize the LLM
    llm = initialize_llm(model, temperature)
    
    # Process each question
    results = []
    correct_count = 0
    
    for question in questions:
        # Get RAG context if enabled
        rag_context = None
        if use_rag:
            rag_context = handbook_index.search(question.question)
        
        # Create prompt and inputs based on question type
        prompt_template, inputs = create_question_prompt(
            question, 
            use_cot=use_cot,
            rag_context=rag_context
        )

        # Prepare the message content
        if question.has_image:
            if model.split("/")[0] == "anthropic":
                # Anthropic can't handle images, convert to text description
                content_parts = []
                for part in inputs["content"]:
                    if part["type"] == "text":
                        content_parts.append(part["text"])
                    elif part["type"] == "image_url":
                        content_parts.append("[Image associated with the question]")
                message_content = "\n".join(content_parts)
            else:
                message_content = inputs["content"]
            
            # Use direct message for image questions
            try:
                response = completion(
                    model=model,
                    messages=[{"role": "user", "content": message_content}],
                    temperature=temperature
                )
                model_answer = response.choices[0].message.content
            except APIError as e:
                logger.warning(f"API Error: {str(e)}")
                model_answer = "Error processing question"
        else:
            # Text-only questions
            prompt_text = prompt_template.format(**inputs)
            response = completion(
                model=model,
                messages=[{"role": "user", "content": prompt_text}],
                temperature=temperature
            )
            model_answer = response.choices[0].message.content

        # Standardize answer format
        model_answer = model_answer.strip().upper()
        
        # Track token usage
        usage = response.usage.dict()
        total_prompt_tokens += usage.get('input_tokens', usage.get('prompt_tokens', 0))
        total_completion_tokens += usage.get('output_tokens', usage.get('completion_tokens', 0))
        total_tokens += usage.get('total_tokens', 0)
        
        # Record the result
        is_correct = extract_final_answer(model_answer) == question.correct_answer
        if is_correct:
            correct_count += 1
            
        result_dict = {
            "question_id": question.id,
            "model_answer": model_answer,
            "correct_answer": question.correct_answer,
            "is_correct": is_correct,
            "has_image": question.has_image,
            "image_path": question.image_path if question.has_image else None,
            "rag_context": rag_context if use_rag else None,
            "token_usage": {
                "input_tokens": usage.get('input_tokens', usage.get('prompt_tokens', 0)),
                "output_tokens": usage.get('output_tokens', usage.get('completion_tokens', 0)),
                "total_tokens": usage.get('total_tokens', 0),
                "input_token_details": {
                    "audio": 0,
                    "cache_read": 0
                },
                "output_token_details": {
                    "audio": 0,
                    "reasoning": usage.get('output_tokens', usage.get('completion_tokens', 0))
                }
            }
        }
            
        results.append(result_dict)
        
        logger.info(f"Question {question.id}: Model answered {model_answer}, Correct: {is_correct}")
    
    # Calculate final results
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # Get pool information
    pool_name, pool_id = get_pool_info(test_file)
    
    provider_id, rest = model.split('/', 1)
    if '/' in rest:
      organization_id, model_id = _normalize_ids(provider_id, *rest.split('/'))
    else:
      organization_id = provider_id
      model_id = rest
    
    return TestResult(
        provider_id=provider_id,
        organization_id=organization_id,
        model_id=model_id,
        test_id=Path(test_file).stem,
        model=model,
        timestamp=start_time.isoformat(),
        questions=results,
        total_questions=len(questions),
        correct_answers=correct_count,
        score_percentage=(correct_count / len(questions)) * 100,
        duration_seconds=duration,
        used_cot=use_cot,
        used_rag=use_rag,
        temperature=temperature,
        token_usage=TokenUsage(
            prompt_tokens=total_prompt_tokens,
            completion_tokens=total_completion_tokens,
            total_tokens=total_tokens,
            input_token_details=TokenUsageDetails(),
            output_token_details=OutputTokenDetails(reasoning=total_completion_tokens)
        ),
        pool_name=pool_name,
        pool_id=pool_id
    )

def save_results(result: TestResult, output_dir: str = "outputs"):
    """Save test results to a JSON file."""
    # Sanitize 'model'
    safe_model = result.model.replace("/", "-").replace("\\", "-")

    os.makedirs(output_dir, exist_ok=True)
    
    # Update the output filename to include 'provider', model name, temperature, CoT and RAG status
    cot_suffix = "_cot" if result.used_cot else ""
    rag_suffix = "_rag" if result.used_rag else ""
    temp_suffix = f"_t{result.temperature:.1f}".replace(".", "p")  # Convert 0.7 to _t0p7
    output_file = Path(output_dir) / f"{safe_model}_{result.test_id}{temp_suffix}{cot_suffix}{rag_suffix}_results.json"
    with open(output_file, 'w') as f:
        json.dump(result.model_dump(), f, indent=2)
    
    logger.info(f"Results saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Evaluate an LLM's performance on an amateur radio exam")
    parser.add_argument("--test-file", required=True, help="Path to the test JSON file")
    parser.add_argument(
        "--model",
        required=True,
        help="Model in format 'provider/model_name' (e.g. 'openrouter/google/palm-2-chat-bison')"
    )
    parser.add_argument("--temperature", type=float, default=0.0, help="Temperature for the LLM")
    parser.add_argument("--output-dir", default="outputs", help="Directory to save results")
    parser.add_argument(
        "--cot",
        action="store_true",
        help="Enable Chain of Thought reasoning"
    )
    parser.add_argument(
        "--rag",
        action="store_true",
        help="Enable Retrieval Augmented Generation using handbook content"
    )
    
    args = parser.parse_args()
    
    try:
        result = evaluate_test(
            args.test_file,
            args.model,
            args.temperature,
            use_cot=args.cot,
            use_rag=args.rag
        )
        save_results(result, args.output_dir)
        
        logger.info(f"\nTest Results for {args.model}:")
        logger.info(f"Score: {result.correct_answers}/{result.total_questions} ({result.score_percentage:.1f}%)")
        logger.info(f"Duration: {result.duration_seconds:.1f} seconds")
        
    except Exception as e:
        logger.error(f"Error during evaluation: {str(e)}")
        raise

if __name__ == "__main__":
    main() 

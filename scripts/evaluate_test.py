#!/usr/bin/env python3
"""
Evaluate an LLM's performance on an amateur radio exam using LangChain.
"""

import argparse
import base64
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
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

class TestResult(BaseModel):
    """Represents the results of a single test evaluation."""
    test_id: str
    model_name: str
    timestamp: str
    questions: List[Dict]
    total_questions: int
    correct_answers: int
    score_percentage: float
    duration_seconds: float

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
        
        if is_general and any(x in question_lower for x in ["figure g7", "figure g-7", "figure g7-1", "figure g-7-1"]):
            q['has_image'] = True
            q['image_path'] = "G7-1.png"
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

def create_question_prompt(question: Question) -> tuple[str, Dict]:
    """Create a prompt for the LLM based on the question."""
    # Convert answers list to choices dict
    choices = {answer.option: answer.text for answer in question.answers}
    
    base_prompt = """You are taking an amateur radio license exam. Please answer the following multiple choice question.
    Only respond with the letter (A, B, C, or D) of your chosen answer. Do not explain your reasoning.

    Question: {question_text}

    Choices:
    A: {choice_a}
    B: {choice_b}
    C: {choice_c}
    D: {choice_d}

    Your answer (just the letter):"""
    
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
                question_text=question.question,
                choice_a=choices['A'],
                choice_b=choices['B'],
                choice_c=choices['C'],
                choice_d=choices['D']
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
            "question_text": question.question,
            "choice_a": choices['A'],
            "choice_b": choices['B'],
            "choice_c": choices['C'],
            "choice_d": choices['D']
        }

def evaluate_test(
    test_file: str,
    model_name: str = "chatgpt-4o-latest",
    temperature: float = 0.0
) -> TestResult:
    """Evaluate an LLM's performance on a test."""
    start_time = datetime.now()
    
    # Load the test
    questions = load_test(test_file)
    
    # Initialize the LLM through LangChain
    llm = ChatOpenAI(
        model_name=model_name,
        temperature=temperature,
        max_tokens=1024
    )
    
    # Process each question
    results = []
    correct_count = 0
    
    for question in questions:
        # Create prompt and inputs based on question type
        prompt_template, inputs = create_question_prompt(question)
        
        if question.has_image:
            # For image-based questions, use the content directly
            from langchain_core.messages import HumanMessage
            response = llm.invoke([HumanMessage(content=inputs["content"])])
            model_answer = response.content.strip().upper()
        else:
            # For text-only questions, use the regular chain
            prompt = PromptTemplate(
                input_variables=list(inputs.keys()),
                template=prompt_template
            )
            chain = LLMChain(llm=llm, prompt=prompt)
            response = chain.invoke(inputs)
            model_answer = response['text'].strip().upper()
        
        # Record the result
        is_correct = model_answer == question.correct_answer
        if is_correct:
            correct_count += 1
            
        results.append({
            "question_id": question.id,
            "model_answer": model_answer,
            "correct_answer": question.correct_answer,
            "is_correct": is_correct,
            "has_image": question.has_image,
            "image_path": question.image_path if question.has_image else None
        })
        
        logger.info(f"Question {question.id}: Model answered {model_answer}, Correct: {is_correct}")
    
    # Calculate final results
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    return TestResult(
        test_id=Path(test_file).stem,
        model_name=model_name,
        timestamp=start_time.isoformat(),
        questions=results,
        total_questions=len(questions),
        correct_answers=correct_count,
        score_percentage=(correct_count / len(questions)) * 100,
        duration_seconds=duration
    )

def save_results(result: TestResult, output_dir: str = "outputs"):
    """Save test results to a JSON file."""
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = Path(output_dir) / f"{result.model_name}_{result.test_id}_results.json"
    with open(output_file, 'w') as f:
        json.dump(result.model_dump(), f, indent=2)
    
    logger.info(f"Results saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Evaluate an LLM's performance on an amateur radio exam")
    parser.add_argument("--test-file", required=True, help="Path to the test JSON file")
    parser.add_argument("--model", default="chatgpt-4o-latest", help="Name of the LLM to use")
    parser.add_argument("--temperature", type=float, default=0.0, help="Temperature for the LLM")
    parser.add_argument("--output-dir", default="outputs", help="Directory to save results")
    
    args = parser.parse_args()
    
    try:
        result = evaluate_test(args.test_file, args.model, args.temperature)
        save_results(result, args.output_dir)
        
        logger.info(f"\nTest Results for {args.model}:")
        logger.info(f"Score: {result.correct_answers}/{result.total_questions} ({result.score_percentage:.1f}%)")
        logger.info(f"Duration: {result.duration_seconds:.1f} seconds")
        
    except Exception as e:
        logger.error(f"Error during evaluation: {str(e)}")
        raise

if __name__ == "__main__":
    main() 
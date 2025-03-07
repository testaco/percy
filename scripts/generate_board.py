#!/usr/bin/env python3

import json
import glob
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from jsonschema import validate, ValidationError

class BoardGenerator:
    def __init__(self):
        self.outputs_dir = Path("outputs")
        self.llmstats_file = Path("data/llmstats.json")
        self.board_file = Path("data/board.json")
        self.llm_stats = self._load_llm_stats()
        
    def _load_llm_stats(self) -> Dict[str, Any]:
        """Load LLM metadata and pricing information"""
        try:
            with open(self.llmstats_file) as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: {self.llmstats_file} not found")
            return {}

    def _calculate_costs(self, result: Dict[str, Any], model_id: str, provider_id: str) -> Dict[str, float]:
        """Calculate costs based on token usage and provider pricing"""
        costs = {
            "total_cost": 0.0,
            "prompt_cost": 0.0,
            "completion_cost": 0.0,
            "cost_per_question": 0.0
        }
        
        if model_id in self.llm_stats:
            model_info = self.llm_stats[model_id]
            for provider in model_info.get("providers", []):
                if provider["provider_id"] == provider_id:
                    prompt_cost = result["token_usage"]["prompt_tokens"] * provider["price_per_input_token"]
                    completion_cost = result["token_usage"]["completion_tokens"] * provider["price_per_output_token"]
                    total_cost = prompt_cost + completion_cost
                    
                    costs.update({
                        "total_cost": total_cost,
                        "prompt_cost": prompt_cost,
                        "completion_cost": completion_cost,
                        "cost_per_question": total_cost / result["total_questions"]
                    })
                    break
        
        return costs

    def _get_license_class(self, test_id: str) -> str:
        """Extract license class from test ID"""
        if test_id.lower().startswith('t'):
            return "technician"
        elif test_id.lower().startswith('g'):
            return "general"
        elif test_id.lower().startswith('e'):
            return "extra"
        return "unknown"

    def _process_test_result(self, result: Dict[str, Any], file_path: str) -> Dict[str, Any]:
        """Process a single test result into board format"""
        model_id = result["model_id"]
        
        # Extract filename without path or extension for test_result_id
        test_result_id = Path(file_path).stem
        
        # Calculate pass/fail and margin
        passing_score = 74.0  # Required passing percentage
        passed = result["score_percentage"] >= passing_score
        margin_to_pass = result["score_percentage"] - passing_score

        # Get model parameters from LLM stats
        model_info = self.llm_stats.get(model_id, {})
        context_window = model_info.get("input_context_size")
        param_count = model_info.get("param_count")

        # Calculate tokens per second
        tokens_per_second = (
            result["token_usage"]["total_tokens"] / result["duration_seconds"]
            if result["duration_seconds"] > 0
            else 0
        )

        return {
            "test_id": result["test_id"],
            "test_result_id": test_result_id,
            "timestamp": result["timestamp"],
            "model_id": model_id,
            "provider_id": result["provider_id"],
            "license_class": self._get_license_class(result["test_id"]),
            "parameters": {
                "temperature": result["temperature"],
                "used_cot": result["used_cot"],
                "used_rag": result["used_rag"],
                "context_window": context_window,
                "param_count": param_count
            },
            "results": {
                "total_questions": result["total_questions"],
                "correct_answers": result["correct_answers"],
                "score_percentage": result["score_percentage"],
                "passed": passed,
                "margin_to_pass": margin_to_pass
            },
            "performance": {
                "duration_seconds": result["duration_seconds"],
                "tokens_per_second": tokens_per_second,
                "total_tokens": result["token_usage"]["total_tokens"],
                "prompt_tokens": result["token_usage"]["prompt_tokens"],
                "completion_tokens": result["token_usage"]["completion_tokens"]
            },
            "costs": self._calculate_costs(result, model_id, result["provider_id"])
        }

    def generate(self):
        """Generate the board data from all test results"""
        # Get all test result files
        result_files = glob.glob(str(self.outputs_dir / "*.json"))
        
        test_results = []
        for file_path in result_files:
            try:
                with open(file_path) as f:
                    result = json.load(f)
                    processed_result = self._process_test_result(result, file_path)
                    test_results.append(processed_result)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                continue

        # Create the final board data
        board_data = {
            "last_updated": datetime.utcnow().isoformat(),
            "test_results": test_results
        }

        # Validate against schema
        schema_path = Path(__file__).parent.parent / "schema" / "board-schema.json"
        try:
            with open(schema_path) as f:
                schema = json.load(f)
            validate(instance=board_data, schema=schema)
        except ValidationError as e:
            print(f"Board schema validation failed: {e.message}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error validating board schema: {str(e)}", file=sys.stderr)
            sys.exit(1)

        # Save to file
        with open(self.board_file, 'w') as f:
            json.dump(board_data, f, indent=2)
        
        print(f"Board data generated with {len(test_results)} test results")

def main():
    generator = BoardGenerator()
    generator.generate()

if __name__ == "__main__":
    main()

import argparse
import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Test configuration for each license class
LICENSE_CONFIG = {
    "technician": {
        "total_questions": 35,
        "pass_percentage": 74,  # 74% to pass
    },
    "general": {
        "total_questions": 35,
        "pass_percentage": 74,
    },
    "extra": {
        "total_questions": 50,
        "pass_percentage": 74,
    }
}

def analyze_results(result_file: str) -> tuple[bool, float, str]:
    """
    Analyze test results and determine if the test was passed.
    
    Args:
        result_file: Path to the results JSON file
        
    Returns:
        tuple containing:
        - bool: Whether the test was passed
        - float: Score percentage
        - str: License class of the test
    """
    with open(result_file) as f:
        results = json.load(f)
    
    # Count correct answers
    correct_count = sum(1 for q in results["questions"] if q["is_correct"])
    total_questions = len(results["questions"])
    score_percentage = (correct_count / total_questions) * 100
    
    # Get test details from test_id to determine license class
    test_file = Path("tests") / f"{results['test_id']}.json"
    with open(test_file) as f:
        test_data = json.load(f)
    license_class = test_data["source_pool"]["license_class"]
    
    # Verify test length matches expected length for license class
    expected_length = LICENSE_CONFIG[license_class]["total_questions"]
    if total_questions != expected_length:
        logger.warning(
            f"Test length ({total_questions}) does not match expected length "
            f"({expected_length}) for {license_class} exam"
        )
    
    # Check if passed based on percentage
    min_percentage = LICENSE_CONFIG[license_class]["pass_percentage"]
    passed = score_percentage >= min_percentage
    
    return passed, score_percentage, license_class

def main():
    parser = argparse.ArgumentParser(description="Analyze amateur radio exam results")
    parser.add_argument("--result-file", required=True, help="Path to the results JSON file")
    args = parser.parse_args()
    
    try:
        passed, score, license_class = analyze_results(args.result_file)
        
        logger.info(f"\nAnalysis Results:")
        logger.info(f"License Class: {license_class.title()}")
        logger.info(f"Score: {score:.1f}%")
        logger.info(f"Required to Pass: {LICENSE_CONFIG[license_class]['pass_percentage']}%")
        logger.info(f"Result: {'PASSED' if passed else 'FAILED'}")
        
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        raise

if __name__ == "__main__":
    main() 
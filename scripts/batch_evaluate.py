from pathlib import Path
from datetime import datetime
import itertools
import json
import yaml
from typing import List, Dict
import glob
import subprocess
import sys

class BatchEvaluation:
    def __init__(self, config_file: str):
        self.config = self._load_config(config_file)
        self.results_dir = Path("outputs/batch_runs")
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.batch_id = self.config.get('batch_name', datetime.now().strftime("%Y%m%d_%H%M%S"))
        self.progress_file = self.results_dir / f"progress_{self.batch_id}.json"
        self.completed_runs = self._load_progress()

    def _load_config(self, config_file: str) -> dict:
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)

    def _load_progress(self) -> List[Dict]:
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        return []

    def _save_progress(self):
        with open(self.progress_file, 'w') as f:
            json.dump(self.completed_runs, f, indent=2)

    def _generate_combinations(self) -> List[Dict]:
        params = self.config['parameters']
        # Handle model-provider pairs separately
        model_providers = params['model_providers']
        other_params = {k: v for k, v in params.items() if k != 'model_providers'}
        
        # Generate base combinations without model/provider
        base_keys = other_params.keys()
        base_values = other_params.values()
        combinations = []
        
        # For each model-provider pair, combine with other parameters
        for base_combo in itertools.product(*base_values):
            base_dict = dict(zip(base_keys, base_combo))
            for model_provider in model_providers:
                combo = base_dict.copy()
                combo['model'] = model_provider['model']
                combinations.append(combo)
                
        return combinations

    def _get_test_files(self) -> List[str]:
        test_files = []
        for pattern in self.config['test_patterns']:
            test_files.extend(glob.glob(pattern))
        return sorted(test_files)

    def _run_evaluation(self, test_file: str, params: Dict) -> None:
        cmd = [
            sys.executable,
            "scripts/evaluate_test.py",
            "--test-file", test_file,
            "--model", params['model'],
            "--temperature", str(params.get('temperature', 0.0))
        ]
        
        if params.get('use_cot'):
            cmd.append("--cot")
        if params.get('use_rag'):
            cmd.append("--rag")
            
        subprocess.run(cmd, check=True)

    def run(self):
        combinations = self._generate_combinations()
        test_files = self._get_test_files()
        
        total_runs = len(combinations) * len(test_files)
        completed = len(self.completed_runs)
        
        print(f"Starting batch {self.batch_id}")
        print(f"Total configurations: {len(combinations)}")
        print(f"Total test files: {len(test_files)}")
        print(f"Total runs needed: {total_runs}")
        
        for combo in combinations:
            for test_file in test_files:
                print(f"Runs completed: {completed}")
                run_config = {
                    "test_file": test_file,
                    **combo
                }
                
                # Skip if already completed
                if run_config in self.completed_runs:
                    continue
                    
                try:
                    self._run_evaluation(test_file, combo)
                    self.completed_runs.append(run_config)
                    self._save_progress()
                except Exception as e:
                    print(f"Error running evaluation: {e}")
                    continue

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Run batch evaluation of models on tests')
    parser.add_argument('--config', required=True, help='Path to batch configuration YAML file')
    args = parser.parse_args()
    
    batch = BatchEvaluation(args.config)
    batch.run()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import json
import yaml
from pathlib import Path
import argparse

def load_llmstats():
    """Load the LLM stats data from the JSON file."""
    try:
        with open('data/llmstats.json') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: data/llmstats.json not found. Run extract_llmstats.py first.")
        return {}

def get_model_provider(model_data):
    """Determine the best provider for a model."""
    org_provider = model_data['organization_id'].lower()
    providers = [p['provider_id'] for p in model_data['providers']]
    
    # Try organization's own provider first
    if org_provider in providers:
        return f"{org_provider}/{model_data['name'].lower()}"
    
    # Fallback to OpenRouter
    if 'openrouter' in providers:
        return f"openrouter/{model_data['name'].lower()}"
    
    return None

def generate_batches(output_dir='.'):
    """Generate batch configuration YAML files based on model categories."""
    llmstats = load_llmstats()
    if not llmstats:
        return
        
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    batches = {
        'proprietary': {'models': [], 'params': {'temperature': [0.0], 'use_cot': [False], 'use_rag': [False]}},
        'small': {'models': [], 'params': {'temperature': [0.3, 0.7], 'use_cot': [True], 'use_rag': [True]}},
        'medium': {'models': [], 'params': {'temperature': [0.3, 0.7], 'use_cot': [False], 'use_rag': [True]}},
        'large': {'models': [], 'params': {'temperature': [0.0], 'use_cot': [False], 'use_rag': [False]}}
    }

    proprietary_orgs = {'openai', 'anthropic', 'xai', 'google', 'amazon', 'microsoft', 'meta'}

    for model_id, model_data in llmstats.items():
        provider = get_model_provider(model_data)
        if not provider:
            continue

        # Check if open model (license-based)
        is_open = model_data.get('license', '').lower() != 'proprietary'
        params = model_data.get('param_count')
        
        # Categorize models
        if model_data['organization_id'].lower() in proprietary_orgs:
            batches['proprietary']['models'].append(provider)
        elif is_open and params:
            if params < 8:
                batches['small']['models'].append(provider)
            elif 8 <= params <= 80:
                batches['medium']['models'].append(provider)
            elif params > 80:
                batches['large']['models'].append(provider)

    # Generate YAML files for each batch
    for batch_name, config in batches.items():
        if not config['models']:
            continue

        yaml_config = {
            'batch_name': f'{batch_name}_eval',
            'parameters': {
                'model_providers': list(set(config['models'])),  # Deduplicate
                **{k: v for k, v in config['params'].items() if v}  # Only include non-empty params
            },
            'test_patterns': [
                'tests/technician_*.json',
                'tests/general_*.json',
                'tests/extra_*.json'
            ]
        }

        output_file = output_path / f'batch_{batch_name}.yaml'
        with open(output_file, 'w') as f:
            yaml.dump(yaml_config, f, sort_keys=False, default_flow_style=False)
            
        print(f"Generated {output_file} with {len(yaml_config['parameters']['model_providers'])} models")

def main():
    parser = argparse.ArgumentParser(description='Generate batch evaluation configurations based on LLM stats')
    parser.add_argument('--output-dir', default='.', help='Directory to save the generated YAML files')
    args = parser.parse_args()
    
    generate_batches(args.output_dir)

if __name__ == '__main__':
    main()

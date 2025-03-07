#!/usr/bin/env python3
import json
import argparse
import os
from pathlib import Path
import subprocess
import sys
from typing import Dict, Any, List
import requests
from datetime import datetime
from dotenv import load_dotenv
from normalize_ids import normalize_ids

def update_submodule(force_yes: bool = False) -> bool:
    """Update the LLMStats submodule if user agrees or force_yes is True."""
    if force_yes:
        response = 'y'
    elif force_yes is False:  # Explicit no
        response = 'n'
    else:
        response = input("Update LLMStats submodule? [y/N] ").lower()
    
    if response == 'y':
        print("Updating LLMStats submodule...")
        result = subprocess.run(
            ["git", "submodule", "update", "--init", "--recursive", "--remote"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"Error updating submodule: {result.stderr}", file=sys.stderr)
            return False
        return True
    return False

def load_json_file(filepath: Path) -> Dict[str, Any]:
    """Load and parse a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}", file=sys.stderr)
        return {}

def fetch_openrouter_models() -> List[Dict]:
    """Fetch OpenRouter models via their API."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Skipping OpenRouter: OPENROUTER_API_KEY not set")
        return []

    try:
        response = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://github.com/your-repo",  # Update with your repo
                "X-Title": "Percy Evaluation"
            }
        )
        response.raise_for_status()
        return response.json()["data"]
    except Exception as e:
        print(f"Error fetching OpenRouter models: {e}")
        return []

def get_provider_info(llmstats_dir: Path) -> Dict[str, Dict[str, Any]]:
    """Get provider information from all sources."""
    providers = {}
    providers_dir = llmstats_dir / "providers"
    
    for provider_file in providers_dir.glob("*/provider.json"):
        provider_name = provider_file.parent.name
        provider_data = load_json_file(provider_file)
        if provider_data:
            providers[provider_name] = provider_data
    
    # Add OpenRouter provider
    openrouter_models = fetch_openrouter_models()
    if openrouter_models:
        providermodels = []
        for model in openrouter_models:
            # Normalize model ID using existing system
            if "/" in model["id"]:
                provider, model_id_part = model["id"].split("/", 1)
                # Use normalize_ids to handle special cases
                normalized_org, normalized_id = normalize_ids(
                    "openrouter", 
                    provider,
                    model_id_part
                )
            else:
                normalized_org = "openrouter"
                normalized_id = model["id"]

            providermodels.append({
                "model_id": normalized_id,
                "price_per_input_token": model["pricing"]["prompt"],
                "price_per_output_token": model["pricing"]["completion"],
                "description": model["description"],
                "context_window": model.get("context_length", 4096),
                "updated_at": datetime.now().isoformat()
            })

        providers["openrouter"] = {
            "provider_id": "openrouter",
            "name": "OpenRouter",
            "website": "https://openrouter.ai",
            "providermodels": providermodels,
            "features": ["chat", "embeddings"],
            "rate_limits": {
                "requests_per_minute": 500,
                "tokens_per_minute": 150000
            }
        }
    
    return providers

def extract_metadata(llmstats_dir: Path) -> Dict[str, Any]:
    """Extract and combine metadata from models and providers."""
    models_dir = llmstats_dir / "models"
    metadata = {}
    providers = get_provider_info(llmstats_dir)
    
    # Traverse all model.json files
    for model_file in models_dir.glob("**/model.json"):
        organization_id = model_file.parent.parent.name
        model_id = model_file.parent.name
        model_data = load_json_file(model_file)
        
        if not model_data:
            continue

        model_data['organization_id'] = organization_id

        # Initialize providers list for this model
        model_data['providers'] = []
        
        # Add provider information if available
        for provider_id, provider_data in providers.items():
            for model_info in provider_data.get('providermodels', []):
                if model_info['model_id'] == model_id:
                    model_data['providers'].append({
                        'provider_id': provider_id,
                        'provider_website': provider_data['website'],
                        'price_per_input_token': model_info['price_per_input_token'],
                        'price_per_output_token': model_info['price_per_output_token'],
                      # Todo  'throughput': model_info['throughput'],
                      # todo  'latency': todo model_info['latency'],
                        'updated_at': model_info['updated_at']
                    })
        
        metadata[model_id] = model_data
    
    return metadata

def main():
    # Ensure we load environment variables from .env file
    load_dotenv()
    
    parser = argparse.ArgumentParser(description='Extract metadata from LLMStats')
    parser.add_argument('-y', action='store_true', help='Automatically update submodule')
    parser.add_argument('-n', action='store_true', help='Skip submodule update')
    args = parser.parse_args()
    
    if args.y and args.n:
        print("Error: Cannot specify both -y and -n", file=sys.stderr)
        sys.exit(1)
    
    force_yes = True if args.y else (False if args.n else None)
    
    # Update submodule if requested
    update_submodule(force_yes)
    
    # Get repository root directory
    repo_root = Path(__file__).parent.parent
    llmstats_dir = repo_root / "LLMStats"
    output_file = repo_root / "data" / "llmstats.json"
    
    # Extract metadata
    metadata = extract_metadata(llmstats_dir)
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Save metadata
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"Metadata saved to {output_file}")

if __name__ == '__main__':
    main()

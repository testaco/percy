"""Module for normalizing LLM provider/model identifiers across services"""

def normalize_ids(provider_id: str, organization_id: str, model_id: str) -> tuple[str, str]:
    """
    Normalize different provider/model identification schemes to canonical forms.
    Handles special cases like OpenRouter proxies for other providers' models.
    """
    # OpenRouter proxy normalization - only current spec example
    if provider_id == 'openrouter' and organization_id == 'google' and model_id == 'gemini-flash-1.5-8b':
        return 'google', 'gemini-1.5-flash-8b'

    if provider_id == 'openrouter' and organization_id == 'meta':
        return 'meta-llama', model_id

    # Add other normalization rules here as needed
    
    # Default case for unrecognized service paths
    return organization_id, model_id

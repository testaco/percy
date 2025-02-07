# Changelog
All notable changes to Percy will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Added comprehensive tests for answer extraction in Chain of Thought responses
- Added Chain of Thought (CoT) reasoning capability with `--cot` flag
- Added CoT usage tracking in test results
- Added `generate_handbook.py` script to generate a comprehensive amateur radio handbook using LLMs
- Added support for generating topic-based study guides from question pools
- Added LLM-based content generation with OpenAI and Anthropic provider support
- Added markdown output format for generated handbook content

### Changed
- Improved answer extraction logic to better handle various response formats
- Enhanced error handling for answer extraction
- Updated documentation with CoT usage examples
- Updated requirements.txt to include necessary LLM dependencies
- Enhanced logging configuration for better debugging and monitoring

## [1.3.0] - 2023-10-05

### Added
- Support for evaluating non-OpenAI models in `evaluate_test.py`.
- Integrated `ChatAnthropic` and `ChatOpenRouter` for Anthropic and OpenRouter providers.
- Added `--provider` argument to select different LLM providers (`openai`, `anthropic`, `ollama`, `openrouter`).
- Implemented provider-specific logic for initializing and invoking LLMs.
- Enhanced image handling logic to accommodate limitations of different providers.
- Updated `README.md` with instructions for setting up API keys for Anthropic, OpenRouter, and Ollama.
- Added usage examples in `README.md` for evaluating models from different providers.
- New dependencies in `requirements.txt` to support Anthropic and community integrations:
  - `langchain-anthropic>=0.0.5`
  - `langchain-community>=0.0.11`
  - `anthropic>=0.4.0`

### Changed
- Refactored `initialize_llm` function to support multiple providers.
- Updated `evaluate_test.py` to handle provider-specific message formatting and response handling.
- Modified prompt creation to account for providers that do not support certain features (e.g., Anthropic models and images).
- Enhanced installation and usage documentation in `README.md` to reflect multi-provider support.

### Fixed
- Improved error handling when unsupported providers are selected.

## [1.2.0] - 2025-01-13

### Added
- Added support for Extra class question pool (2024-2028)
- Added support for Extra class diagrams (pages 1-3) in evaluation script
- Added handling for multiple figures per diagram page in Extra class

## [1.1.0] - 2025-01-13

### Added
- Added support for General class question pool (2023-2027)
- Added support for General class image G7-1.png in evaluation script

### Changed
- Updated test filenames to include license class and version (e.g., general-2023-2027-test_20250113_130333.json)
- Modified extract_pool.py to automatically detect license class and version from filename
- Enhanced evaluate_test.py to handle both JPG and PNG image formats
- Improved figure reference detection in evaluate_test.py to handle variations (e.g., "Figure G7-1", "Figure G-7")

## [1.0.0] - 2025-01-13

### Added
- Initial project structure and documentation
- README with project overview, folder structure, and usage instructions
- Script to convert DOCX question pools to JSON format (`extract_pool.py`)
- Script to generate randomized tests (`generate_test.py`) that selects one question from each group
- Virtual environment setup instructions
- Requirements.txt with python-docx dependency
- LangChain-based evaluation system (`evaluate_test.py`) for testing LLM performance
- Added dependencies: langchain, langchain-openai, python-dotenv, pydantic, pillow
- Added multimodal support for image-based questions (T1.jpg, T2.jpg, T3.jpg)
- Added langchain-community for image handling
- Added analysis script (`analyze_results.py`) to determine pass/fail status based on license class criteria

### Changed
- Made --input and --output parameters required in extract_pool.py
- Updated README with detailed usage instructions for extract_pool.py
- Modified generate_test.py to require explicit question pool file input
- Enhanced test output to include source question pool information
- Updated evaluate_test.py to use GPT-4 Vision for image-based questions
- Updated analysis script to handle different test lengths for each license class (35 questions for Technician/General, 50 for Extra)

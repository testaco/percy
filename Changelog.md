# Changelog
All notable changes to Percy will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
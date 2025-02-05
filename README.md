### README for Percy – Amateur Radio Test Bot

---

## Overview

**Percy** is a project aimed at building an automated system to evaluate the performance of various large language models (LLMs) from multiple providers (OpenAI, Anthropic, Ollama, OpenRouter) on the official amateur radio exams (Technician, General, and Extra). The goal is to see which models can pass each level of the exam with a measurable degree of certainty.

The project follows these steps:

1. **Extract the Question Pool**  
   Implement a system to extract and structure the NCVEC question pools for all license classes.

2. **Randomized Test Generation**  
   Randomly generate tests according to NCVEC exam rules:
   - Technician: 35 questions
   - General: 35 questions
   - Extra: 50 questions
   Each test ensures balanced question selection by category.

3. **Question-Answering System**  
   Build a system that presents the questions (including those with diagrams) to different LLMs and retrieves their answers.

4. **Result Analysis**  
   Determine whether the LLM passed or failed the test based on official pass/fail criteria (74% required to pass) for each license class.

---

## Folder Structure

```
/percy
│
├── /data               # Contains the processed question pools (JSON format)
│   ├── technician.json
│   ├── general.json
│   └── extra.json
│
├── /scripts            # Scripts for processing question pools, generating tests, evaluating models, and analyzing results
│   ├── extract_pool.py
│   ├── generate_test.py
│   ├── evaluate_test.py
│   └── analyze_results.py
│
├── /tests              # Generated tests for different license classes
│   ├── test_001.json
│   ├── test_002.json
│   └── ...
│
├── /outputs            # Results and logs of model evaluations
│   ├── gpt4-mini_test_001_results.json
│   ├── gpt4o_test_002_results.json
│   └── ...
│
└── README.md           # Project documentation
```

---

## Installation Guide

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/testaco/percy.git
   cd percy
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   # or
   .\venv\Scripts\activate  # On Windows
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up API Keys for LLM Providers**

   Depending on which LLM providers you intend to use, set up the necessary API keys as environment variables:

   - **OpenAI:**

     ```bash
     export OPENAI_API_KEY='your-openai-api-key'
     ```

   - **Anthropic:**

     ```bash
     export ANTHROPIC_API_KEY='your-anthropic-api-key'
     ```

   - **OpenRouter:**

     ```bash
     export OPENROUTER_API_KEY='your-openrouter-api-key'
     ```

   - **Ollama:**

     - Ensure Ollama is installed and running locally. Visit [Ollama's documentation](https://ollama.ai/docs/installation) for setup instructions.

---

## Usage

### Convert Question Pool to JSON

The `extract_pool.py` script converts a DOCX question pool file into a structured JSON format. Both input and output paths are required.

```bash
python scripts/extract_pool.py --input <docx_file> --output <json_file>
```

Example:
```bash
python scripts/extract_pool.py --input data/technician-2022-2026.docx --output data/technician-2022-2026.json
```

Additional options:
- `--test`: Run test to verify first question format
- `--debug`: Enable debug output

### Generate a Test

This script randomly selects one question from each group in the question pool and saves the test in the `/tests` folder.

```bash
python scripts/generate_test.py --pool-file <json_file>
```

Example:
```bash
python scripts/generate_test.py --pool-file data/technician-2022-2026.json
```

Additional options:
- `--output-dir`: Directory to save the generated test (default: tests)

### Evaluate a Model on a Specific Test

This script runs the specified model from the chosen provider on a generated test and saves the results in the `/outputs` folder.

```bash
python scripts/evaluate_test.py --test-file <test_file> --model <model_name> --provider <provider_name>
```

**Parameters:**

- `--test-file`: Path to the test JSON file.
- `--model`: Name of the LLM model to use.
- `--provider`: LLM provider to use (`openai`, `anthropic`, `ollama`, or `openrouter`).
- `--temperature`: (Optional) Temperature setting for the LLM (default: `0.0`).

**Examples:**

- **Using OpenAI GPT-4:**

  ```bash
  python scripts/evaluate_test.py --test-file tests/technician_test.json --model gpt-4 --provider openai
  ```

- **Using Anthropic Claude-v1:**

  ```bash
  python scripts/evaluate_test.py --test-file tests/general_test.json --model claude-v1 --provider anthropic
  ```

- **Using OpenRouter ChatGPT-4:**

  ```bash
  python scripts/evaluate_test.py --test-file tests/extra_test.json --model chatgpt-4o-latest --provider openrouter
  ```

- **Using Ollama Llama2:**

  ```bash
  python scripts/evaluate_test.py --test-file tests/technician_test.json --model llama2 --provider ollama
  ```

**Note:**

- Ensure you have the necessary API keys and environment variables set for each provider.
- For **OpenAI**, set `OPENAI_API_KEY`.
- For **Anthropic**, set `ANTHROPIC_API_KEY`.
- For **OpenRouter**, set `OPENROUTER_API_KEY`.
- **Ollama** is assumed to be running locally and may require additional setup.

### Analyze Results

This script processes the output from the model evaluation and determines whether the model passed or failed the exam based on the specific rules for that license class (74% required to pass).

Run the script with the result file:

```bash
python scripts/analyze_results.py --result-file outputs/gpt4-mini_test_001_results.json
```

The script will output:
- License class of the test
- Score achieved
- Required passing score (74%)
- Whether the model passed or failed

---

## Contribution

Feel free to open issues and submit pull requests as the project evolves. The README will be updated over time as we build out the features.

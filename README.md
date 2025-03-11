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
├── /question_pools     # Contains the processed question pools (JSON format)
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
├── /schema             # JSON schemas for data validation
│   ├── question-pool.schema.json
│   ├── test-result.schema.json
│   ├── llmstats-schema.json
│   └── board-schema.json      # Schema for aggregated leaderboard data
│
└── README.md           # Project documentation
```

---

## Question Pool JSON Schema

The question pool JSON files follow a strict schema defined in `schema/question-pool.schema.json`. This schema enforces:

- Valid license class values ("technician", "general", "extra")
- Version format (YYYY-YYYY)
- Question ID patterns (e.g., T1A01 for Technician)
- Group ID patterns (e.g., T1A)
- Required fields and data types
- Answer option constraints (A, B, C, D)
- Exactly 4 answer choices per question

The schema ensures consistency and validates the structure of all question pool JSON files.

Example question pool JSON that follows the schema:
```json
{
  "license_class": "technician",
  "version": "2022-2026",
  "group_titles": {
    "T1A": "Purpose and permissible use of the Amateur Radio Service",
    "T1B": "Authorized frequencies; Frequency allocations",
    "T1C": "Operator licensing"
  },
  "questions": [
    {
      "id": "T1A01",
      "group": "T1A",
      "question": "Which of the following is a purpose of the Amateur Radio Service as stated in the FCC rules and regulations?",
      "answers": [
        {
          "option": "A",
          "text": "Providing personal radio communications for as many citizens as possible"
        },
        {
          "option": "B",
          "text": "Providing communications during international emergencies only"
        },
        {
          "option": "C",
          "text": "Advancing skills in the technical and communication phases of the radio art"
        },
        {
          "option": "D",
          "text": "All of these choices are correct"
        }
      ],
      "correct_answer": "C"
    }
  ]
}
```

## Test Result JSON Schema

The test result JSON files follow a strict schema defined in `schema/test-result.schema.json`. This schema enforces:

- Required fields like provider, model name, test ID, etc.
- Timestamp format and validation
- Question result structure including token usage
- Token usage tracking at both question and test level
- Support for RAG context tracking
- Support for image handling in questions

Example test result that follows the schema:
```json
{
  "provider": "openai",
  "test_id": "tech_001",
  "model_name": "gpt-4",
  "timestamp": "2024-01-20T15:30:45Z",
  "questions": [
    {
      "question_id": "T1A01",
      "model_answer": "C",
      "correct_answer": "C", 
      "is_correct": true,
      "has_image": false,
      "token_usage": {
        "input_tokens": 245,
        "output_tokens": 89,
        "total_tokens": 334,
        "input_token_details": {
          "audio": 0,
          "cache_read": 0
        },
        "output_token_details": {
          "audio": 0,
          "reasoning": 89
        }
      }
    }
  ],
  "total_questions": 35,
  "correct_answers": 30,
  "score_percentage": 85.71,
  "duration_seconds": 87.5,
  "used_cot": true,
  "used_rag": false,
  "temperature": 0.0,
  "token_usage": {
    "prompt_tokens": 8575,
    "completion_tokens": 3115,
    "total_tokens": 11690
  },
  "pool_name": "technician-2022-2026",
  "pool_id": "T"
}
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
python scripts/extract_pool.py --input question_pools/technician-2022-2026.docx --output question_pools/technician-2022-2026.json
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
python scripts/generate_test.py --pool-file question_pools/technician-2022-2026.json
```

Additional options:
- `--output-dir`: Directory to save the generated test (default: tests)

### Evaluate a Model on a Specific Test

This script runs the specified model from the chosen provider on a generated test and saves the results in the `/data/evaluations` folder.

```bash
python scripts/evaluate_test.py --test-file <test_file> --model <model_name>
```

**Parameters:**

- `--test-file`: Path to the test JSON file.
- `--model`: Name of the LLM model to use.
- `--temperature`: (Optional) Temperature setting for the LLM (default: `0.0`).
- `--cot`: (Optional) Enable Chain of Thought reasoning mode.

**Example with Chain of Thought:**

```bash
python scripts/evaluate_test.py --test-file tests/technician_test.json --model openai/gpt-4 --cot
```

**Examples:**

- **Using OpenAI GPT-4:**

  ```bash
  python scripts/evaluate_test.py --test-file tests/technician_test.json --model openai/gpt-4
  ```

- **Using Anthropic Claude-v1:**

  ```bash
  python scripts/evaluate_test.py --test-file tests/general_test.json --model anthropic/claude-3-sonnet
  ```

- **Using OpenRouter ChatGPT-4:**

  ```bash
  python scripts/evaluate_test.py --test-file tests/extra_test.json --model openrouter/chatgpt-4o-latest
  ```

**Note:**

- Ensure you have the necessary API keys and environment variables set for each provider.  Follow the docs for litellm for specific providers.
- For **OpenAI**, set `OPENAI_API_KEY`.
- For **Anthropic**, set `ANTHROPIC_API_KEY`.
- For **OpenRouter**, set `OPENROUTER_API_KEY`.

### Batch Evaluation

The batch evaluation system allows running multiple tests with different configurations using a YAML configuration file:

```bash
python scripts/batch_evaluate.py --config batch_config.yaml
```

**Configuration File Format:**

The configuration file should be in YAML format with the following structure:

```yaml
# Example batch_config.yaml
batch_name: "initial_evaluation_run"  # Unique identifier for this batch

parameters:
  model_providers:  # Valid model-provider pairs
    - "openai/gpt-4"
    - "openai/gpt-3.5-turbo" 
    - "anthropic/claude-3-sonnet"
    - "anthropic/claude-2"
    - "ollama/llama2"
  temperature:
    - 0.0
    - 0.7
  use_cot:
    - true
    - false
  use_rag:
    - true
    - false

test_patterns:
  - "tests/technician_*.json"
  - "tests/general_*.json"
```

The script will:
1. Use the specified batch name for organizing results
2. Generate combinations using only valid model-provider pairs
3. Run each combination on all matching test files
4. Save progress continuously to allow resuming interrupted runs
5. Store results in `outputs/batch_runs/`

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

### Extract LLM Metadata

The `extract_llmstats.py` script aggregates metadata about LLM models and their providers from the LLMStats submodule into a single JSON dataset. This data includes model capabilities, context sizes, benchmark scores, and provider-specific information like pricing and throughput.

```bash
# Update submodule and extract stats
python scripts/extract_llmstats.py -y

# Skip submodule update and extract stats
python scripts/extract_llmstats.py -n

# Prompt for submodule update
python scripts/extract_llmstats.py
```

The script:
1. Optionally updates the LLMStats submodule
2. Extracts model metadata from `LLMStats/models/<creator>/<model_id>/model.json` files
3. Combines with provider data from `LLMStats/providers/<provider>/provider.json` files
4. Saves aggregated dataset to `data/llmstats.json`

The output follows the schema defined in `schema/llmstats-schema.json` and includes:
- Model capabilities (context sizes, multimodal support, etc.)
- Benchmark scores across various datasets
- Provider-specific information (pricing, throughput, latency)
- Links to documentation, papers, and model weights

This metadata is used to:
- Calculate costs for test evaluations
- Track model capabilities and limitations
- Compare performance across benchmarks
- Reference model documentation and resources

### Generate and Index Handbook Content

#### Generate Content Using LLMs

The `generate_handbook.py` script creates an educational handbook by generating comprehensive content for specified sub-element groups using a Large Language Model (LLM).

```bash
python scripts/generate_handbook.py --patterns <patterns> --provider <provider_name> --model-name <model_name> --temperature <temperature>
```

**Parameters:**

- `--patterns`: List of glob patterns to filter groups (e.g., `"*1*"`, `"G2A"`). This determines which question groups will be used to generate content.
- `--provider`: LLM provider to use (`openai` or `anthropic`). Default is `openai`.
- `--model-name`: Name of the LLM model to use. Defaults to `gpt-4` for OpenAI or the appropriate model for Anthropic.
- `--temperature`: Sampling temperature for the LLM (default: `0.7`).

**Examples:**

- **Using OpenAI GPT-4 to generate content for all sub-element groups containing '1':**

  ```bash
  python scripts/generate_handbook.py --patterns "*1*" --provider openai --model-name "gpt-4" --temperature 0.7
  ```

- **Using Anthropic's Claude-v1 to generate content for group G2A:**

  ```bash
  python scripts/generate_handbook.py --patterns "G2A" --provider anthropic --model-name "claude-v1" --temperature 0.7
  ```

**Output:**

The generated content will be saved as markdown files in the `handbook` directory, one file per sub-element group (e.g., `handbook/T1A.md`).

**Notes:**

- Ensure you have the necessary API keys and environment variables set for the chosen LLM provider.
  - For **OpenAI**, set `OPENAI_API_KEY`.
  - For **Anthropic**, set `ANTHROPIC_API_KEY`.
- The generated markdown files can be converted to other formats (e.g., PDF, EPUB) using Pandoc or similar tools.

#### Index Handbook Content for RAG

The `handbook_indexer.py` script creates a FAISS vector store index of the handbook content for use in RAG (Retrieval Augmented Generation) pipelines.

```bash
# Build the index (creates cache/handbook_index_*.npz)
python scripts/handbook_indexer.py

# Force rebuild index
python scripts/handbook_indexer.py --force

# Test search functionality
python scripts/handbook_indexer.py --query "What is impedance matching?"
```

**Features:**
- Uses FAISS for efficient similarity search
- Caches computed embeddings to avoid redundant processing
- Splits content into chunks for fine-grained retrieval
- Supports semantic search queries

### Generate PDF Handbook

The `publish_handbook.py` script converts the markdown handbook content into a formatted PDF document, organizing content by chapters.

```bash
python scripts/publish_handbook.py
```

**Requirements:**
- Pandoc must be installed on your system
- PDFtk must be installed on your system

**Output:**
- Individual chapter PDFs in `handbook/chapters/`
- Complete handbook at `handbook/handbook.pdf`

The script:
1. Generates individual chapter PDFs from markdown files
2. Applies consistent formatting using pandoc
3. Combines all chapters into a single handbook.pdf

---

### Generate Leaderboard Data Board

The `generate_board.py` script aggregates test results and LLM metadata into a comprehensive board dataset for the leaderboard application. This data includes test performance, costs, and model capabilities.

```bash
python scripts/generate_board.py
```

The script:
1. Processes all JSON files in the `outputs` directory
2. Combines test results with LLM metadata from `data/llmstats.json`
3. Calculates additional metrics like:
   - Pass/fail status (74% required)
   - Margin to passing score
   - Token usage and costs
   - Performance metrics (tokens/second)
4. Saves the aggregated board data to `data/board.json`

The output follows the schema defined in `schema/board-schema.json` and includes:
- Test results with detailed metrics
- Model parameters and capabilities
- Performance statistics
- Cost analysis per test
- License class information

This board data powers the leaderboard web application's:
- Overall rankings
- Performance comparisons
- Cost analysis
- Detailed test result views

---

## Contribution

Feel free to open issues and submit pull requests as the project evolves. The README will be updated over time as we build out the features.

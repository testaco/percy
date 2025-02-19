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

## Question Pool JSON Schema

The question pool JSON files follow this schema:

```json
{
  "license_class": string,        // "technician", "general", or "extra"
  "version": string,             // Version/year range of the question pool
  "group_titles": {              // Mapping of group IDs to their titles
    string: string               // e.g., "T1A": "Purpose and permissible use..."
  },
  "questions": [
    {
      "id": string,              // Question ID (e.g., "T1A01")
      "group": string,           // Sub-element group ID (e.g., "T1A")
      "question": string,        // The actual question text
      "answers": [
        {
          "option": string,      // Answer option (A, B, C, or D)
          "text": string         // Text of the answer choice
        }
      ],
      "correct_answer": string   // The correct answer option (A, B, C, or D)
    }
  ]
}
```

Example:
```json
{
  "license_class": "technician",
  "version": "2022-2026",
  "group_titles": {
    "T1A": "Purpose and permissible use of the Amateur Radio Service; Operator/primary station license grant"
  },
  "questions": [
    {
      "id": "T1A01",
      "group": "T1A",
      "question": "Which of the following is part of the Basis and Purpose of the Amateur Radio Service?",
      "answers": [
        {
          "option": "A",
          "text": "Providing personal radio communications for as many citizens as possible"
        },
        {
          "option": "B", 
          "text": "Providing communications for international non-profit organizations"
        },
        {
          "option": "C",
          "text": "Advancing skills in the technical and communication phases of the radio art"
        },
        {
          "option": "D",
          "text": "All these choices are correct"
        }
      ],
      "correct_answer": "C"
    }
  ]
}
```

## Test Result JSON Schema

Test result files follow this schema:

```json
{
  "test_id": string,            // Unique identifier for the test
  "license_class": string,      // "technician", "general", or "extra"
  "model": string,              // Name of the LLM model used
  "provider": string,           // Provider of the LLM (openai, anthropic, etc.)
  "temperature": float,         // Temperature setting used
  "use_cot": boolean,          // Whether Chain of Thought was used
  "use_rag": boolean,          // Whether RAG was used
  "timestamp": string,          // ISO format timestamp of the evaluation
  "results": [
    {
      "question_id": string,    // Question ID (e.g., "T1A01")
      "group": string,          // Sub-element group ID (e.g., "T1A")
      "model_answer": string,   // The answer option chosen by the model (A, B, C, or D)
      "correct_answer": string, // The correct answer option
      "is_correct": boolean,    // Whether the model's answer was correct
      "response": string,       // Full response from the model
      "duration": float        // Time taken to answer in seconds
    }
  ],
  "summary": {
    "total_questions": integer, // Total number of questions
    "correct_answers": integer, // Number of correct answers
    "score": float,            // Score as percentage
    "passed": boolean,         // Whether the score meets passing criteria
    "total_duration": float    // Total time taken in seconds
  }
}
```

Example:
```json
{
  "test_id": "tech_001",
  "license_class": "technician",
  "model": "gpt-4",
  "provider": "openai",
  "temperature": 0.0,
  "use_cot": true,
  "use_rag": false,
  "timestamp": "2024-01-20T15:30:45Z",
  "results": [
    {
      "question_id": "T1A01",
      "group": "T1A",
      "model_answer": "C",
      "correct_answer": "C",
      "is_correct": true,
      "response": "Let me think about this step by step...",
      "duration": 2.5
    }
  ],
  "summary": {
    "total_questions": 35,
    "correct_answers": 30,
    "score": 85.71,
    "passed": true,
    "total_duration": 87.5
  }
}
```

---

## Leaderboard Web Application

The project includes a Next.js-based web application for visualizing test results and model performance. The leaderboard app provides:

- Overall leaderboard showing model performance across all tests
- Detailed evaluation pages for individual test results
- Filtering by model, provider, license class, and other parameters
- Performance charts and visualizations
- Chain of Thought (CoT) reasoning display when available

### Running the Leaderboard App

```bash
# Navigate to the leaderboard directory
cd leaderboard

# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at http://localhost:3000

### Leaderboard Features

- **Real-time Updates**: Automatically reflects new test results as they're generated
- **Performance Metrics**: Shows pass rates, average scores, and timing data
- **Filtering & Search**: Filter results by model, provider, license class, and more
- **Detailed Views**: Examine individual test attempts and Chain of Thought reasoning
- **Data Visualization**: Charts showing performance trends and comparisons
- **Mobile Responsive**: Fully responsive design using shadcn/ui components

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
- `--cot`: (Optional) Enable Chain of Thought reasoning mode.

**Example with Chain of Thought:**

```bash
python scripts/evaluate_test.py --test-file tests/technician_test.json --model gpt-4 --provider openai --cot
```

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
    - model: "gpt-4"
      provider: "openai"
    - model: "gpt-3.5-turbo"
      provider: "openai"
    - model: "claude-v1"
      provider: "anthropic"
    - model: "claude-2"
      provider: "anthropic"
    - model: "llama2"
      provider: "ollama"
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

## Contribution

Feel free to open issues and submit pull requests as the project evolves. The README will be updated over time as we build out the features.

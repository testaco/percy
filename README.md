### README for Percy – Amateur Radio Test Bot

---

## Overview

**Percy** is a project aimed at building an automated system to evaluate the performance of various large language models (LLMs) on the official amateur radio exams (Technician, General, and Extra). The goal is to see which models can pass each level of the exam with a measurable degree of certainty.

The project follows these steps:

1. **Extract the Question Pool**  
   Implement a system to extract and structure the NCVEC question pools for all license classes.

2. **Randomized Test Generation**  
   Randomly generate tests according to NCVEC exam rules, ensuring balanced question selection by category.

3. **Question-Answering System**  
   Build a system that presents the questions (including those with diagrams) to different LLMs and retrieves their answers.

4. **Automated Scoring and Result Logging**  
   Evaluate the LLMs' answers, score the tests, and log the results for analysis.

5. **Result Analysis**  
   Determine whether the LLM passed or failed the test based on official pass/fail criteria for each license class.

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

2. **Set Up the Environment**  
   Install the required dependencies using Python's package manager:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Initial Setup**  
   Extract and process the question pools:
   ```bash
   python scripts/extract_pool.py
   ```

---

## Usage

### Generate a Test

This script randomly selects questions from the pool and saves the test in the `/tests` folder.

```bash
python scripts/generate_test.py --license-class technician
```

### Evaluate a Model on a Specific Test

This script runs the specified model on a generated test and saves the results in the `/outputs` folder.

```bash
python scripts/evaluate_test.py --model gpt4o-mini --test-file tests/test_001.json
```

### Analyze Results

This script processes the output from the model evaluation and determines whether the model passed or failed the exam based on the specific rules for that license class.


#### Usage

Run the script with the result file and license class as inputs:

```bash
python scripts/analyze_results.py --result-file outputs/gpt4-mini_test_001_results.json --license-class technician
```

The script will output a message indicating whether the model passed or failed the test.

---

## Contribution

Feel free to open issues and submit pull requests as the project evolves. The README will be updated over time as we build out the features.
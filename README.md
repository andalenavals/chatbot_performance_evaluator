# Chatbot Performance Evaluator

A modular Python project for comparing chatbots that take text in and return text out.

## Current chatbot types

- **Full context bot**: injects the entire domain knowledge file into the prompt.
- **Strict semantic match bot**: finds the most similar question in the FAQ set and returns its expected answer without generation.

## Features

- FAQ input from CSV with `question` and `expected_answer`
- per-row metric storage in CSV and JSONL
- configurable LLM-as-judge metrics
- Streamlit app for chatting and inspecting benchmark rows
- Sphinx documentation and GitHub Pages workflow

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
python examples/run_benchmark.py
streamlit run app/main.py
```

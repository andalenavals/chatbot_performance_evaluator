# Chatbot Performance Evaluator

A modular framework for validating chatbots against FAQ-style datasets.

The project compares two bot strategies:
- **full-context prompting**, where an LLM answers using a shared domain-knowledge file
- **strict semantic match**, where the system retrieves the answer attached to the most similar FAQ question

It records row-level outputs, deterministic metrics, and LLM-as-a-judge metrics, then exposes the results through CSV, JSONL, and a Streamlit inspection app.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
python examples/run_benchmark.py
streamlit run app/main.py
```

## Documentation

Build the docs locally:

```bash
pip install -e .[docs]
sphinx-build -b html docs docs/_build/html
```

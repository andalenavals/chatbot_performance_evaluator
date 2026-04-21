# Chatbot Evaluation Framework

A modular, extensible framework to **systematically evaluate, benchmark, and validate chatbot systems**.

---
## Documentation

Full documentation is available here:

[![Docs](https://img.shields.io/badge/docs-online-blue)](https://andalenavals.github.io/chatbot_performance_evaluator/overview.html)


## 🚀 Why this project?

As LLM-powered systems scale, **evaluation becomes the bottleneck**.

- How do you know a chatbot is correct?
- How do you prevent regressions?
- How do you test safety?
- How do you compare models or prompts?

This project provides a **structured evaluation framework** that answers those questions.

---

## 🧠 What it does

- Evaluate chatbot outputs against expected answers
- Run multiple bots on the same dataset
- Compare configurations (prompt, model, etc.)
- Use LLMs as judges for:
  - safety
  - relevance
  - faithfulness
- Track [metrics](https://andalenavals.github.io/chatbot_performance_evaluator/metrics.html#deterministic-metrics) per question

---

## 📦 What’s included

- Full-context chatbot
- Semantic match chatbot
- CSV-based evaluation pipeline
- LLM judge system (OpenAI or Ollama)
- Streamlit visualization app
- Sphinx documentation (with API docs)
- Adversarial dataset for safety testing

---

## Project structure

```text
chatbot_performance_evaluator/
├── app/
│   └── main.py
│   └── services.py
├── configs/
│   ├── bots/
│   │   ├── prompts/
│   │   │   └── full_context_prompt.txt
│   │   ├── full_context_deepseek.json
│   │   ├── full_context_gpt4o_mini.json
│   │   └── semantic_match.json
│   ├── judges/
│   │   ├── prompts/
│   │   │   ├── relevance_faithfulness.txt
│   │   │   └── safety_robustness.txt
│   │   ├── relevance_faithfulness.json
│   │   └── safety_robustness.json
│   └── models/
│       ├── deepseek-r1.json
│       └── gpt-4o-mini.json
│       └── qwen3.json
├── data/
│   ├── domain_knowledge.txt
│   └── faq.csv
│   └── faq_adversarial.csv
├── examples/
│   └── run_benchmark.py
├── outputs/
├── src/
│   └── chatbot_eval/
└── tests/
└── docs/
```

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

For OpenAI-backed bots or judges:

```bash
pip install -e .[dev,openai]
export OPENAI_API_KEY=your_key_here
```

## Quickstart

```bash
python examples/run_benchmark.py
streamlit run app/main.py
```

## Config notes

- Model-specific parameters live in `configs/models/*.json`
- Bot prompt files live in `configs/bots/prompts/`
- Judge prompt files live in `configs/judges/prompts/`
- Judge configs default to `deepseek-r1`
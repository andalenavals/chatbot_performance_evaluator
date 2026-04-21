# Chatbot Performance Evaluator

A config-driven Python project for evaluating text-in/text-out chatbots against CSV benchmarks.

## What is included

- CSV input with `question` and `expected_answer`
- Two bot implementations only:
  - `full_context`: sends the full domain knowledge plus one reusable prompt to an LLM
  - `strict_semantic_match`: embeds the incoming question and returns the expected answer from the most similar benchmark row
- Metric groups:
  - Accuracy & Correctness
  - Quality of Communication
  - Operational Performance
  - LLM-as-a-judge metrics for Safety & Robustness and Relevance & Faithfulness
- Streamlit app for side-by-side chat and sample inspection
- Prompt files kept outside `src/`
- Model-specific config files with provider-specific request options

## Project structure

```text
chatbot_performance_evaluator/
├── app/
│   └── app.py
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
├── data/
│   ├── domain_knowledge.txt
│   └── sample_eval.csv
├── examples/
│   └── run_benchmark.py
├── outputs/
├── src/
│   └── chatbot_eval/
└── tests/
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

## Run benchmark

```bash
python examples/run_benchmark.py
```

Outputs are written to `outputs/`:

- `results_detailed.csv`
- `results_detailed.jsonl`
- `summary_by_bot.csv`

## Run app

```bash
streamlit run app/app.py
```

## Config notes

- Model-specific parameters live in `configs/models/*.json`
- Bot prompt files live in `configs/bots/prompts/`
- Judge prompt files live in `configs/judges/prompts/`
- Judge configs default to `deepseek-r1`
- If a judge config points to OpenAI but the API key is unavailable, the builder falls back to the default local DeepSeek judge model

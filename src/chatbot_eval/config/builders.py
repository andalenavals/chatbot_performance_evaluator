from __future__ import annotations

from pathlib import Path

from chatbot_eval.clients.ollama import OllamaChatClient
from chatbot_eval.clients.openai_client import OpenAIChatClient
from chatbot_eval.config.judges import JudgeConfig
from chatbot_eval.config.models import ModelConfig
from chatbot_eval.metrics.llm_judge import LLMJudgeMetric
from chatbot_eval.utils.files import load_json


def load_model_config(path: str | Path) -> ModelConfig:
    return ModelConfig(**load_json(path))


def load_judge_config(path: str | Path) -> JudgeConfig:
    return JudgeConfig(**load_json(path))


def build_chat_client(model_config: ModelConfig):
    provider = model_config.provider.lower()
    if provider == 'ollama':
        return OllamaChatClient(model=model_config.model, temperature=model_config.temperature, request_kwargs=model_config.request_kwargs)
    if provider == 'openai':
        api_key = model_config.credentials.get('api_key', '')
        if not api_key:
            raise ValueError('Missing OpenAI API key in model config credentials.api_key')
        return OpenAIChatClient(model=model_config.model, api_key=api_key, temperature=model_config.temperature, request_kwargs=model_config.request_kwargs)
    raise ValueError(f'Unsupported provider: {model_config.provider}')


def build_judge_metric(project_root: str | Path, judge_config_path: str | Path) -> LLMJudgeMetric:
    project_root = Path(project_root)
    judge_config = load_judge_config(judge_config_path)
    model_cfg = load_model_config(project_root / judge_config.model_config)
    try:
        client = build_chat_client(model_cfg)
    except ValueError:
        fallback = load_model_config(project_root / 'configs/models/deepseek-r1.json')
        client = build_chat_client(fallback)
    return LLMJudgeMetric(name=judge_config.name, llm_client=client, prompt_path=project_root / judge_config.prompt_path, debug=judge_config.debug)

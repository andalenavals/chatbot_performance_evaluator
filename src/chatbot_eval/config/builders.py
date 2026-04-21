from __future__ import annotations

from pathlib import Path

from chatbot_eval.bots.factory import build_bot
from chatbot_eval.clients.ollama import OllamaChatClient, OllamaEmbeddingClient
from chatbot_eval.clients.openai import OpenAIChatClient, OpenAIEmbeddingClient
from chatbot_eval.metrics.llm_judge import LLMJudgeMetric

from .loader import load_bot_config, load_judge_config, load_model_config
from .schema import ModelConfig


def build_chat_client(model_config: ModelConfig):
    if model_config.provider == "ollama":
        return OllamaChatClient(model_config=model_config, base_url=model_config.credentials.get("base_url", "http://localhost:11434"))
    if model_config.provider == "openai":
        return OpenAIChatClient(model_config=model_config)
    raise ValueError(f"Unsupported chat model provider: {model_config.provider}")


def build_embedding_client(model_config: ModelConfig):
    if model_config.provider == "ollama":
        return OllamaEmbeddingClient(model_config=model_config, base_url=model_config.credentials.get("base_url", "http://localhost:11434"))
    if model_config.provider == "openai":
        return OpenAIEmbeddingClient(model_config=model_config)
    raise ValueError(f"Unsupported embedding model provider: {model_config.provider}")


def build_bot_from_config(config_path: str | Path):
    return build_bot(load_bot_config(config_path), load_model_config, build_chat_client, build_embedding_client)


def build_judge_metric(config_path: str | Path, default_local_model_path: str | Path | None = None) -> LLMJudgeMetric:
    judge_config = load_judge_config(config_path)
    model_config = load_model_config(judge_config.model_config)
    try:
        client = build_chat_client(model_config)
    except RuntimeError:
        if not default_local_model_path:
            raise
        model_config = load_model_config(default_local_model_path)
        client = build_chat_client(model_config)
    return LLMJudgeMetric(
        name=judge_config.name,
        judge_client=client,
        prompt_path=judge_config.prompt_path,
        score_range=tuple(judge_config.score_range),
        debug=judge_config.debug,
        judge_model_name=model_config.name,
    )

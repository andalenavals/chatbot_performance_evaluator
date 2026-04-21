from __future__ import annotations

from pathlib import Path
from typing import Callable

from chatbot_eval.data.csv_loader import load_samples_from_csv
from chatbot_eval.retrieval.semantic_matcher import SemanticMatcher

from .full_context import FullContextBot
from .semantic_match import StrictSemanticMatchBot


def build_bot(bot_config, load_model_config: Callable, build_chat_client: Callable, build_embedding_client: Callable):
    if bot_config.bot_type == "full_context":
        if not bot_config.chat_model_config or not bot_config.prompt_path or not bot_config.domain_knowledge_path:
            raise ValueError("full_context bot config requires chat_model_config, prompt_path, and domain_knowledge_path")
        model_config = load_model_config(bot_config.chat_model_config)
        return FullContextBot(
            name=bot_config.name,
            chat_client=build_chat_client(model_config),
            model_config=model_config,
            prompt_path=Path(bot_config.prompt_path),
            domain_knowledge_path=Path(bot_config.domain_knowledge_path),
            bot_config=bot_config,
        )

    if bot_config.bot_type == "strict_semantic_match":
        if not bot_config.embedding_model_config or not bot_config.dataset_path:
            raise ValueError("strict_semantic_match bot config requires embedding_model_config and dataset_path")
        model_config = load_model_config(bot_config.embedding_model_config)
        samples = load_samples_from_csv(bot_config.dataset_path)
        matcher = SemanticMatcher(build_embedding_client(model_config), samples)
        return StrictSemanticMatchBot(
            name=bot_config.name,
            matcher=matcher,
            model_config=model_config,
            bot_config=bot_config,
        )

    raise ValueError(f"Unsupported bot_type: {bot_config.bot_type}")

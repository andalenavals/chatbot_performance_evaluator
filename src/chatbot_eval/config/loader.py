from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

from .schema import BotConfig, JudgeConfig, ModelConfig

_ENV_PATTERN = re.compile(r"\$\{([^}]+)\}")


def _resolve_env(value: Any) -> Any:
    if isinstance(value, str):
        return _ENV_PATTERN.sub(lambda match: os.environ.get(match.group(1), ""), value)
    if isinstance(value, list):
        return [_resolve_env(item) for item in value]
    if isinstance(value, dict):
        return {key: _resolve_env(item) for key, item in value.items()}
    return value


def load_json(path: str | Path) -> dict[str, Any]:
    file_path = Path(path)
    data = json.loads(file_path.read_text(encoding="utf-8"))
    return _resolve_env(data)


def _resolve_optional_path(base: Path, value: str | None) -> Path | None:
    if not value:
        return None
    candidate = Path(value)
    return candidate if candidate.is_absolute() else (base / candidate).resolve()


def load_model_config(path: str | Path) -> ModelConfig:
    file_path = Path(path).resolve()
    data = load_json(file_path)
    return ModelConfig(
        name=data["name"],
        provider=data["provider"],
        model_name=data["model_name"],
        temperature=float(data.get("temperature", 0.0)),
        request_options=data.get("request_options", {}),
        credentials=data.get("credentials", {}),
        source_path=file_path,
    )


def load_bot_config(path: str | Path) -> BotConfig:
    file_path = Path(path).resolve()
    data = load_json(file_path)
    base = file_path.parent.parent
    return BotConfig(
        name=data["name"],
        bot_type=data["bot_type"],
        chat_model_config=_resolve_optional_path(base, data.get("chat_model_config")),
        embedding_model_config=_resolve_optional_path(base, data.get("embedding_model_config")),
        prompt_path=_resolve_optional_path(base, data.get("prompt_path")),
        domain_knowledge_path=_resolve_optional_path(base, data.get("domain_knowledge_path")),
        dataset_path=_resolve_optional_path(base, data.get("dataset_path")),
        semantic_threshold=float(data.get("semantic_threshold", 0.0)),
        metadata=data.get("metadata", {}),
        source_path=file_path,
    )


def load_judge_config(path: str | Path) -> JudgeConfig:
    file_path = Path(path).resolve()
    data = load_json(file_path)
    base = file_path.parent.parent
    return JudgeConfig(
        name=data["name"],
        model_config=_resolve_optional_path(base, data["model_config"]),
        prompt_path=_resolve_optional_path(base, data["prompt_path"]),
        score_range=list(data.get("score_range", [1, 5])),
        debug=bool(data.get("debug", False)),
        source_path=file_path,
    )

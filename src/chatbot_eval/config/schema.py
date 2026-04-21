from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict


@dataclass(slots=True)
class ModelConfig:
    name: str
    provider: str
    model_name: str
    temperature: float = 0.0
    request_options: Dict[str, Any] = field(default_factory=dict)
    credentials: Dict[str, Any] = field(default_factory=dict)
    source_path: Path | None = None

    def request_payload(self) -> Dict[str, Any]:
        payload = dict(self.request_options)
        if self.provider == "openai":
            payload.setdefault("temperature", self.temperature)
        elif self.provider == "ollama":
            options = dict(payload.get("options", {}))
            options.setdefault("temperature", self.temperature)
            payload["options"] = options
        return payload


@dataclass(slots=True)
class BotConfig:
    name: str
    bot_type: str
    chat_model_config: Path | None = None
    embedding_model_config: Path | None = None
    prompt_path: Path | None = None
    domain_knowledge_path: Path | None = None
    dataset_path: Path | None = None
    semantic_threshold: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    source_path: Path | None = None


@dataclass(slots=True)
class JudgeConfig:
    name: str
    model_config: Path
    prompt_path: Path
    score_range: list[float] = field(default_factory=lambda: [1, 5])
    debug: bool = False
    source_path: Path | None = None

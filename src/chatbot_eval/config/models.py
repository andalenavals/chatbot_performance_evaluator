from __future__ import annotations

"""Configuration models for provider-specific LLM settings."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ModelConfig:
    """Configuration for a single provider-backed model."""

    name: str
    provider: str
    model: str
    temperature: float = 0.0
    credentials: dict[str, Any] = field(default_factory=dict)
    request_kwargs: dict[str, Any] = field(default_factory=dict)

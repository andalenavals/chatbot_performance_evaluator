from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ModelConfig:
    name: str
    provider: str
    model: str
    temperature: float = 0.0
    credentials: dict[str, Any] = field(default_factory=dict)
    request_kwargs: dict[str, Any] = field(default_factory=dict)

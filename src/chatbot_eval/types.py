from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(slots=True)
class Sample:
    question: str
    expected_answer: str


@dataclass(slots=True)
class Completion:
    text: str
    thinking: str | None = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class BotResult:
    answer: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class MetricResult:
    name: str
    score: float
    details: Dict[str, Any] = field(default_factory=dict)

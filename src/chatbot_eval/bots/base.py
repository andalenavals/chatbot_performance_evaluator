from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Protocol


@dataclass(slots=True)
class BotResult:
    answer: str
    latency_ms: float
    metadata: Dict[str, Any] = field(default_factory=dict)


class Chatbot(Protocol):
    name: str

    def answer(self, question: str) -> BotResult: ...

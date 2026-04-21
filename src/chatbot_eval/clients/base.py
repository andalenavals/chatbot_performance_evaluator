from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Protocol


@dataclass(slots=True)
class ChatCompletion:
    text: str
    thinking: str | None = None
    raw: Dict[str, Any] = field(default_factory=dict)


class ChatClient(Protocol):
    def generate(self, prompt: str, *, system_prompt: str | None = None) -> ChatCompletion: ...


class EmbeddingClient(Protocol):
    def embed_texts(self, texts: list[str]) -> list[list[float]]: ...

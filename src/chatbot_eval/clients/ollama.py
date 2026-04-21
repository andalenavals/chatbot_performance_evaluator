from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

import requests

from chatbot_eval.config.schema import ModelConfig
from .base import ChatCompletion


@dataclass(slots=True)
class OllamaChatClient:
    model_config: ModelConfig
    base_url: str = "http://localhost:11434"
    timeout: int = 300

    def generate(self, prompt: str, *, system_prompt: str | None = None) -> ChatCompletion:
        payload: Dict[str, Any] = {
            "model": self.model_config.model_name,
            "stream": False,
            "messages": [],
        }
        if system_prompt:
            payload["messages"].append({"role": "system", "content": system_prompt})
        payload["messages"].append({"role": "user", "content": prompt})
        payload.update(self.model_config.request_payload())

        response = requests.post(
            f"{self.base_url.rstrip('/')}/api/chat",
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()
        message = data.get("message", {})
        return ChatCompletion(
            text=message.get("content", "").strip(),
            thinking=(message.get("thinking") or "").strip() or None,
            raw=data,
        )


@dataclass(slots=True)
class OllamaEmbeddingClient:
    model_config: ModelConfig
    base_url: str = "http://localhost:11434"
    timeout: int = 300

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        payload: Dict[str, Any] = {
            "model": self.model_config.model_name,
            "input": texts,
        }
        payload.update(self.model_config.request_payload())
        response = requests.post(
            f"{self.base_url.rstrip('/')}/api/embed",
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("embeddings", [])

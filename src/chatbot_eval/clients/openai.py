from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from chatbot_eval.config.schema import ModelConfig
from .base import ChatCompletion


@dataclass(slots=True)
class OpenAIChatClient:
    model_config: ModelConfig

    def __post_init__(self) -> None:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("OpenAI support requires `pip install -e .[openai]`") from exc
        api_key = self.model_config.credentials.get("api_key")
        if not api_key:
            raise RuntimeError("Missing OpenAI API key in model config credentials.api_key")
        base_url = self.model_config.credentials.get("base_url")
        self._client = OpenAI(api_key=api_key, base_url=base_url)

    def generate(self, prompt: str, *, system_prompt: str | None = None) -> ChatCompletion:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        payload: Dict[str, Any] = {
            "model": self.model_config.model_name,
            "messages": messages,
        }
        payload.update(self.model_config.request_payload())
        response = self._client.chat.completions.create(**payload)
        content = response.choices[0].message.content or ""
        return ChatCompletion(text=content.strip(), raw=response.model_dump())


@dataclass(slots=True)
class OpenAIEmbeddingClient:
    model_config: ModelConfig

    def __post_init__(self) -> None:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("OpenAI support requires `pip install -e .[openai]`") from exc
        api_key = self.model_config.credentials.get("api_key")
        if not api_key:
            raise RuntimeError("Missing OpenAI API key in model config credentials.api_key")
        base_url = self.model_config.credentials.get("base_url")
        self._client = OpenAI(api_key=api_key, base_url=base_url)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        response = self._client.embeddings.create(model=self.model_config.model_name, input=texts)
        return [item.embedding for item in response.data]

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict

import requests

from chatbot_eval.types import Completion


@dataclass(slots=True)
class OllamaChatClient:
    model: str
    base_url: str = 'http://localhost:11434'
    temperature: float = 0.0
    request_kwargs: dict[str, Any] = field(default_factory=dict)
    timeout: int = 300

    def generate(self, prompt: str) -> Completion:
        url = f"{self.base_url.rstrip('/')}/api/chat"
        payload: Dict[str, Any] = {
            'model': self.model,
            'messages': [{'role': 'user', 'content': prompt}],
            'stream': False,
            'options': {'temperature': self.temperature},
        }
        for key, value in self.request_kwargs.items():
            if key == 'options' and isinstance(value, dict):
                payload['options'].update(value)
            else:
                payload[key] = value
        response = requests.post(url, json=payload, timeout=self.timeout)
        if not response.ok:
            raise RuntimeError(
                f'Ollama request failed: status={response.status_code}, model={self.model}, url={url}, body={response.text}'
            )
        data = response.json()
        message = data.get('message', {})
        return Completion(text=message.get('content', '') or '', thinking=message.get('thinking'), raw=data)

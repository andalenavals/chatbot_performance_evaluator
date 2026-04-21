from __future__ import annotations

"""OpenAI-compatible chat client wrapper."""

from dataclasses import dataclass, field
from typing import Any, Dict

import requests

from chatbot_eval.types import Completion


@dataclass(slots=True)
class OpenAIChatClient:
    """Wrapper around the OpenAI chat completions endpoint."""

    model: str
    api_key: str
    base_url: str = 'https://api.openai.com/v1'
    temperature: float = 0.0
    request_kwargs: dict[str, Any] = field(default_factory=dict)
    timeout: int = 300

    def generate(self, prompt: str) -> Completion:
        url = f"{self.base_url.rstrip('/')}/chat/completions"
        payload: Dict[str, Any] = {
            'model': self.model,
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': self.temperature,
        }
        payload.update(self.request_kwargs)
        response = requests.post(
            url,
            headers={'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'},
            json=payload,
            timeout=self.timeout,
        )
        if not response.ok:
            raise RuntimeError(
                f'OpenAI request failed: status={response.status_code}, model={self.model}, body={response.text}'
            )
        data = response.json()
        return Completion(text=data['choices'][0]['message']['content'] or '', raw=data)

from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path

from chatbot_eval.config.schema import BotConfig, ModelConfig
from chatbot_eval.utils.files import read_text
from chatbot_eval.utils.templating import render_template

from .base import BotResult


@dataclass(slots=True)
class FullContextBot:
    name: str
    chat_client: object
    model_config: ModelConfig
    prompt_path: Path
    domain_knowledge_path: Path
    bot_config: BotConfig

    def answer(self, question: str) -> BotResult:
        prompt = render_template(
            self.prompt_path,
            question=question,
            domain_knowledge=read_text(self.domain_knowledge_path),
        )
        start = time.perf_counter()
        completion = self.chat_client.generate(prompt)
        latency_ms = (time.perf_counter() - start) * 1000
        metadata = {
            "bot_type": "full_context",
            "bot_config": str(self.bot_config.source_path) if self.bot_config.source_path else self.name,
            "chat_model": self.model_config.name,
            "thinking": completion.thinking,
            "raw_response": completion.raw,
        }
        return BotResult(answer=completion.text, latency_ms=latency_ms, metadata=metadata)

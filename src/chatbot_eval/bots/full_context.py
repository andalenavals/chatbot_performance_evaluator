from __future__ import annotations

"""Bot implementation that injects the full domain knowledge into one prompt."""

from dataclasses import dataclass
from pathlib import Path

from chatbot_eval.bots.base import BaseBot
from chatbot_eval.types import BotResult
from chatbot_eval.utils.files import load_text, render_template


@dataclass(slots=True)
class FullContextBot(BaseBot):
    """A simple generative bot backed by one prompt and the full knowledge base."""

    name: str
    chat_client: object
    prompt_path: str | Path
    domain_knowledge_path: str | Path

    def answer(self, question: str) -> BotResult:
        domain_knowledge = load_text(self.domain_knowledge_path)
        prompt = render_template(
            self.prompt_path,
            domain_knowledge=domain_knowledge,
            question=question,
        )
        completion = self.chat_client.generate(prompt)
        return BotResult(
            answer=completion.text,
            metadata={
                'bot_type': 'full_context',
                'prompt_path': str(self.prompt_path),
                'domain_knowledge_path': str(self.domain_knowledge_path),
                'thinking': completion.thinking,
                'raw_completion': completion.raw,
            },
        )

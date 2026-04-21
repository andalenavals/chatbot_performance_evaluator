from __future__ import annotations

"""Abstract chatbot interface used by the evaluator and the app."""

from abc import ABC, abstractmethod

from chatbot_eval.types import BotResult


class BaseBot(ABC):
    """Minimal text-in/text-out bot contract."""

    name: str

    @abstractmethod
    def answer(self, question: str) -> BotResult:
        """Return the bot response for ``question``."""
        raise NotImplementedError

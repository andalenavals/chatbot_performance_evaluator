from __future__ import annotations

from abc import ABC, abstractmethod

from chatbot_eval.types import BotResult


class BaseBot(ABC):
    name: str

    @abstractmethod
    def answer(self, question: str) -> BotResult:
        raise NotImplementedError

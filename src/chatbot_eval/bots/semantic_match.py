from __future__ import annotations

import time
from dataclasses import dataclass

from chatbot_eval.config.schema import BotConfig, ModelConfig
from chatbot_eval.retrieval.semantic_matcher import SemanticMatcher

from .base import BotResult


@dataclass(slots=True)
class StrictSemanticMatchBot:
    name: str
    matcher: SemanticMatcher
    model_config: ModelConfig
    bot_config: BotConfig

    def answer(self, question: str) -> BotResult:
        start = time.perf_counter()
        match = self.matcher.best_match(question)
        latency_ms = (time.perf_counter() - start) * 1000
        return BotResult(
            answer=match.sample.expected_answer,
            latency_ms=latency_ms,
            metadata={
                "bot_type": "strict_semantic_match",
                "bot_config": str(self.bot_config.source_path) if self.bot_config.source_path else self.name,
                "embedding_model": self.model_config.name,
                "matched_question": match.sample.question,
                "matched_row_id": match.sample.row_id,
                "similarity": match.score,
                "match_method": match.method,
            },
        )

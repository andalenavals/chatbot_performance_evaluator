from __future__ import annotations

from dataclasses import dataclass

from .base import MetricResult


@dataclass(slots=True)
class CommunicationClarityMetric:
    name: str = "quality_communication_clarity"

    def score(self, sample, bot_result) -> MetricResult:
        text = bot_result.answer.strip()
        word_count = len(text.split())
        has_sentence = 1.0 if any(p in text for p in ".!?") else 0.0
        concise_bonus = 1.0 if 1 <= word_count <= 80 else 0.5
        score = min(5.0, round((has_sentence + concise_bonus) * 2.5, 2))
        return MetricResult(name=self.name, score=score, details={"word_count": word_count})

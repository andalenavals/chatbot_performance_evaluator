from __future__ import annotations

from dataclasses import dataclass

from .base import MetricResult


def _normalize(text: str) -> str:
    return " ".join(text.lower().strip().split())


@dataclass(slots=True)
class ExactMatchMetric:
    name: str = "accuracy_exact_match"

    def score(self, sample, bot_result) -> MetricResult:
        exact = 1.0 if _normalize(sample.expected_answer) == _normalize(bot_result.answer) else 0.0
        return MetricResult(name=self.name, score=exact)

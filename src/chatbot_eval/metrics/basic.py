from __future__ import annotations

"""Deterministic baseline metrics used by the evaluator."""

import re
from dataclasses import dataclass

from chatbot_eval.types import BotResult, MetricResult, Sample


def _normalize(text: str) -> str:
    return re.sub(r'\s+', ' ', text.strip().lower())


def _tokens(text: str) -> set[str]:
    return {token.strip(".,!?;:()[]{}\"'").lower() for token in text.split() if token.strip()}


@dataclass(slots=True)
class ExactMatchMetric:
    """Binary exact-match score after simple normalization."""

    name: str = 'exact_match'

    def score(self, sample: Sample, bot_result: BotResult) -> MetricResult:
        value = 1.0 if _normalize(sample.expected_answer) == _normalize(bot_result.answer) else 0.0
        return MetricResult(name=self.name, score=value)


@dataclass(slots=True)
class KeywordRecallMetric:
    """Recall of expected-answer tokens present in the generated answer."""

    name: str = 'keyword_recall'

    def score(self, sample: Sample, bot_result: BotResult) -> MetricResult:
        expected = _tokens(sample.expected_answer)
        got = _tokens(bot_result.answer)
        score = len(expected & got) / len(expected) if expected else 0.0
        return MetricResult(name=self.name, score=round(score, 4))


@dataclass(slots=True)
class AnswerLengthMetric:
    """Character length of the answer as a communication proxy."""

    name: str = 'answer_length_chars'

    def score(self, sample: Sample, bot_result: BotResult) -> MetricResult:
        return MetricResult(name=self.name, score=float(len(bot_result.answer)))


@dataclass(slots=True)
class PolitenessMetric:
    """Simple heuristic scoring polite or helpful markers in the answer."""

    name: str = 'politeness'

    def score(self, sample: Sample, bot_result: BotResult) -> MetricResult:
        text = bot_result.answer.lower()
        markers = ['please', 'sorry', 'happy to help', 'can help']
        found = sum(1 for marker in markers if marker in text)
        score = min(found / 2.0, 1.0)
        return MetricResult(name=self.name, score=round(score, 4))

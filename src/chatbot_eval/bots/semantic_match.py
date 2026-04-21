from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from pathlib import Path

from chatbot_eval.bots.base import BaseBot
from chatbot_eval.io.csv_loader import load_samples_from_csv
from chatbot_eval.types import BotResult, Sample


def _tokenize(text: str) -> set[str]:
    return {token.strip(".,!?;:()[]{}\"'").lower() for token in text.split() if token.strip()}


def _cosine_overlap(a: str, b: str) -> float:
    ta = _tokenize(a)
    tb = _tokenize(b)
    if not ta or not tb:
        return 0.0
    vocab = ta | tb
    va = [1.0 if token in ta else 0.0 for token in vocab]
    vb = [1.0 if token in tb else 0.0 for token in vocab]
    dot = sum(x * y for x, y in zip(va, vb))
    norm_a = sqrt(sum(x * x for x in va))
    norm_b = sqrt(sum(y * y for y in vb))
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0


@dataclass(slots=True)
class StrictSemanticMatchBot(BaseBot):
    name: str
    faq_csv_path: str | Path

    def answer(self, question: str) -> BotResult:
        samples = load_samples_from_csv(self.faq_csv_path)
        best_sample: Sample | None = None
        best_score = -1.0
        for sample in samples:
            score = _cosine_overlap(question, sample.question)
            if score > best_score:
                best_score = score
                best_sample = sample
        answer = best_sample.expected_answer if best_sample else ''
        return BotResult(answer=answer, metadata={'bot_type': 'strict_semantic_match', 'faq_csv_path': str(self.faq_csv_path), 'matched_question': best_sample.question if best_sample else None, 'similarity': round(best_score, 4) if best_sample else None})

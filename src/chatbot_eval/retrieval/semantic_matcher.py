from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Iterable, Sequence

from chatbot_eval.data.models import EvalSample


@dataclass(slots=True)
class SemanticMatch:
    sample: EvalSample
    score: float
    method: str


class SemanticMatcher:
    def __init__(self, embedding_client, samples: Sequence[EvalSample]):
        self.embedding_client = embedding_client
        self.samples = list(samples)
        self._questions = [sample.question for sample in self.samples]
        self._embeddings = []
        self._mode = "lexical"
        if self.samples:
            try:
                self._embeddings = self.embedding_client.embed_texts(self._questions)
                if self._embeddings:
                    self._mode = "embedding"
            except Exception:
                self._embeddings = []
                self._mode = "lexical"

    def best_match(self, question: str) -> SemanticMatch:
        if self._mode == "embedding":
            query_embedding = self.embedding_client.embed_texts([question])[0]
            best_score = -1.0
            best_sample = self.samples[0]
            for sample, embedding in zip(self.samples, self._embeddings):
                score = cosine_similarity(query_embedding, embedding)
                if score > best_score:
                    best_score = score
                    best_sample = sample
            return SemanticMatch(sample=best_sample, score=best_score, method="embedding")

        query_tokens = tokenize(question)
        best_score = -1.0
        best_sample = self.samples[0]
        for sample in self.samples:
            score = jaccard_similarity(query_tokens, tokenize(sample.question))
            if score > best_score:
                best_score = score
                best_sample = sample
        return SemanticMatch(sample=best_sample, score=best_score, method="lexical")


def cosine_similarity(a: Iterable[float], b: Iterable[float]) -> float:
    a_list = list(a)
    b_list = list(b)
    numerator = sum(x * y for x, y in zip(a_list, b_list))
    denominator = math.sqrt(sum(x * x for x in a_list)) * math.sqrt(sum(y * y for y in b_list))
    if denominator == 0:
        return 0.0
    return numerator / denominator


def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def jaccard_similarity(a: set[str], b: set[str]) -> float:
    union = a | b
    if not union:
        return 0.0
    return len(a & b) / len(union)

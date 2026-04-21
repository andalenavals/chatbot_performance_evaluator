from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(slots=True)
class Evaluator:
    metrics: list

    def evaluate_sample(self, sample, bot) -> dict:
        bot_result = bot.answer(sample.question)
        metric_results = [metric.score(sample, bot_result) for metric in self.metrics]
        return {
            "row_id": sample.row_id,
            "question": sample.question,
            "expected_answer": sample.expected_answer,
            "generated_answer": bot_result.answer,
            "bot_name": bot.name,
            "bot_metadata": bot_result.metadata,
            "metrics": {metric.name: metric.score for metric in metric_results},
            "metric_details": {metric.name: metric.details for metric in metric_results},
        }

    def evaluate_dataset(self, samples: Iterable, bots: Iterable) -> list[dict]:
        rows: list[dict] = []
        samples_list = list(samples)
        for bot in bots:
            for sample in samples_list:
                rows.append(self.evaluate_sample(sample, bot))
        return rows

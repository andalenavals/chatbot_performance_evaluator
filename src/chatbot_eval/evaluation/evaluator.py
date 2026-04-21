from __future__ import annotations

import json
from dataclasses import dataclass
from time import perf_counter

from chatbot_eval.types import BotResult, Sample


@dataclass(slots=True)
class Evaluator:
    metrics: list[object]

    def evaluate_sample(self, sample: Sample, bot) -> dict:
        metric_values: dict[str, float] = {}
        metric_details: dict[str, dict] = {}
        started = perf_counter()
        try:
            bot_result = bot.answer(sample.question)
            latency_ms = (perf_counter() - started) * 1000.0
            metric_values['latency_ms'] = round(latency_ms, 3)
            for metric in self.metrics:
                try:
                    result = metric.score(sample, bot_result)
                    metric_values[result.name] = result.score
                    metric_details[result.name] = result.details
                except Exception as exc:
                    metric_values[getattr(metric, 'name', metric.__class__.__name__)] = 0.0
                    metric_details[getattr(metric, 'name', metric.__class__.__name__)] = {'error': str(exc)}
            generated_answer = bot_result.answer
            bot_metadata = bot_result.metadata
        except Exception as exc:
            generated_answer = ''
            bot_metadata = {'error': str(exc)}
            metric_values['latency_ms'] = round((perf_counter() - started) * 1000.0, 3)
            metric_details['bot_error'] = {'error': str(exc)}
        return {
            'bot_name': bot.name,
            'question': sample.question,
            'expected_answer': sample.expected_answer,
            'generated_answer': generated_answer,
            'metrics_json': json.dumps(metric_values, ensure_ascii=False),
            'metric_details_json': json.dumps(metric_details, ensure_ascii=False),
            'bot_metadata_json': json.dumps(bot_metadata, ensure_ascii=False),
        }

    def evaluate_dataset(self, samples: list[Sample], bots: list[object]) -> list[dict]:
        rows: list[dict] = []
        for bot in bots:
            for sample in samples:
                rows.append(self.evaluate_sample(sample, bot))
        return rows

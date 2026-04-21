from __future__ import annotations

from dataclasses import dataclass

from .base import MetricResult


@dataclass(slots=True)
class LatencyMetric:
    name: str = "operational_latency_ms"

    def score(self, sample, bot_result) -> MetricResult:
        return MetricResult(name=self.name, score=round(bot_result.latency_ms, 2))

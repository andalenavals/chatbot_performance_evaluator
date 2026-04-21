from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Protocol


@dataclass(slots=True)
class MetricResult:
    name: str
    score: float
    details: Dict[str, Any] = field(default_factory=dict)


class Metric(Protocol):
    name: str

    def score(self, sample, bot_result) -> MetricResult: ...

from __future__ import annotations

"""Core shared data structures used throughout the evaluation pipeline."""

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(slots=True)
class Sample:
    """One evaluation row loaded from the FAQ CSV file."""

    question: str
    expected_answer: str


@dataclass(slots=True)
class Completion:
    """Raw completion returned by a chat backend.

    Attributes
    ----------
    text:
        Final model output shown to the user.
    thinking:
        Optional reasoning trace, when the provider exposes one.
    raw:
        Provider-native payload kept for debugging.
    """

    text: str
    thinking: str | None = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class BotResult:
    """Answer returned by a bot together with trace metadata."""

    answer: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class MetricResult:
    """Result produced by one metric for one question-answer pair."""

    name: str
    score: float
    details: Dict[str, Any] = field(default_factory=dict)

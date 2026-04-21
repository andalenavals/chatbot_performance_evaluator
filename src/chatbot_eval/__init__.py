"""Framework for benchmarking text-in/text-out chatbots.

The package provides a small but extensible toolkit to compare chatbot
strategies against FAQ-style datasets, record detailed row-level metrics,
and inspect results through both a CLI workflow and a Streamlit app.
"""

from .evaluation.evaluator import Evaluator
from .types import BotResult, Completion, MetricResult, Sample

__all__ = [
    "BotResult",
    "Completion",
    "Evaluator",
    "MetricResult",
    "Sample",
]

__version__ = "0.2.0"

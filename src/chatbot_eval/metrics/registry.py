from __future__ import annotations

"""Metric registry helpers used by the CLI and the Streamlit app."""

from pathlib import Path

from chatbot_eval.config.builders import build_judge_metric
from chatbot_eval.metrics.basic import (
    AnswerLengthMetric,
    ExactMatchMetric,
    KeywordRecallMetric,
    PolitenessMetric,
)


def build_default_metrics(project_root: str | Path) -> list[object]:
    """Build the default deterministic and judge-based metric suite."""

    project_root = Path(project_root)
    metrics: list[object] = [
        ExactMatchMetric(),
        KeywordRecallMetric(),
        AnswerLengthMetric(),
        PolitenessMetric(),
        build_judge_metric(project_root, project_root / 'configs/judges/safety_robustness.json'),
        build_judge_metric(project_root, project_root / 'configs/judges/relevance_faithfulness.json'),
    ]
    return metrics

from __future__ import annotations

from pathlib import Path

from chatbot_eval.config.builders import build_judge_metric

from .accuracy import ExactMatchMetric
from .communication import CommunicationClarityMetric
from .operational import LatencyMetric


def build_default_metrics(project_root: Path):
    judges_dir = project_root / "configs" / "judges"
    models_dir = project_root / "configs" / "models"
    return [
        ExactMatchMetric(),
        CommunicationClarityMetric(),
        LatencyMetric(),
        build_judge_metric(judges_dir / "safety_robustness.json", default_local_model_path=models_dir / "deepseek-r1.json"),
        build_judge_metric(judges_dir / "relevance_faithfulness.json", default_local_model_path=models_dir / "deepseek-r1.json"),
    ]

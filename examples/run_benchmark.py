from __future__ import annotations

from pathlib import Path

from chatbot_eval.config.builders import build_bot_from_config
from chatbot_eval.data.csv_loader import load_samples_from_csv
from chatbot_eval.evaluation.evaluator import Evaluator
from chatbot_eval.metrics.registry import build_default_metrics
from chatbot_eval.reports.writers import write_outputs
from chatbot_eval.utils.files import list_json_files


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    samples = load_samples_from_csv(project_root / "data" / "sample_eval.csv")
    bot_paths = list_json_files(project_root / "configs" / "bots")
    bots = []
    for path in bot_paths:
        try:
            bots.append(build_bot_from_config(path))
        except RuntimeError as exc:
            print(f"Skipping {path.name}: {exc}")
    evaluator = Evaluator(metrics=build_default_metrics(project_root))
    if not bots:
        raise RuntimeError("No bot configs could be loaded. Check local Ollama availability or OPENAI_API_KEY.")
    rows = evaluator.evaluate_dataset(samples=samples, bots=bots)
    write_outputs(rows, project_root / "outputs")
    print(f"Wrote {len(rows)} detailed rows to {project_root / 'outputs'}")


if __name__ == "__main__":
    main()

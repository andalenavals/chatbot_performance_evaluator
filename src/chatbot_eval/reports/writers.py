from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from chatbot_eval.utils.files import write_jsonl


def write_outputs(rows: list[dict], output_dir: str | Path) -> None:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    flat_rows = []
    for row in rows:
        flat = {
            "row_id": row["row_id"],
            "bot_name": row["bot_name"],
            "question": row["question"],
            "expected_answer": row["expected_answer"],
            "generated_answer": row["generated_answer"],
            "bot_metadata_json": json.dumps(row.get("bot_metadata", {}), ensure_ascii=False),
            "metric_details_json": json.dumps(row.get("metric_details", {}), ensure_ascii=False),
        }
        flat.update(row.get("metrics", {}))
        flat_rows.append(flat)

    detailed_df = pd.DataFrame(flat_rows)
    detailed_df.to_csv(output_path / "results_detailed.csv", index=False)
    write_jsonl(output_path / "results_detailed.jsonl", rows)

    metric_columns = sorted({key for row in rows for key in row.get("metrics", {})})
    summary_df = detailed_df.groupby("bot_name")[metric_columns].mean(numeric_only=True).reset_index()
    summary_df.to_csv(output_path / "summary_by_bot.csv", index=False)

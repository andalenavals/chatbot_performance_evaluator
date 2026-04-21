from __future__ import annotations

"""Reporting utilities for row-level results and aggregate summaries."""

import csv
import json
from pathlib import Path


def write_rows_csv(rows: list[dict], path: str | Path) -> None:
    """Persist evaluation rows to CSV."""

    if not rows:
        return
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with open(out, 'w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_rows_jsonl(rows: list[dict], path: str | Path) -> None:
    """Persist evaluation rows to JSON Lines."""

    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, 'w', encoding='utf-8') as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + '\n')


def summarize_by_bot(rows: list[dict]) -> list[dict]:
    """Average numeric metrics per bot across all rows."""

    groups: dict[str, dict[str, list[float]]] = {}
    for row in rows:
        bot = row['bot_name']
        metrics = json.loads(row['metrics_json'])
        bucket = groups.setdefault(bot, {})
        for name, value in metrics.items():
            bucket.setdefault(name, []).append(float(value))
    summary = []
    for bot, metric_values in groups.items():
        item = {'bot_name': bot}
        for name, values in metric_values.items():
            item[name] = round(sum(values) / len(values), 4) if values else 0.0
        summary.append(item)
    return summary

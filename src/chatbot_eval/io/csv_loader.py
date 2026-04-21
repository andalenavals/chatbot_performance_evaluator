from __future__ import annotations

import csv
from pathlib import Path
from typing import List

from chatbot_eval.types import Sample


def load_samples_from_csv(path: str | Path) -> List[Sample]:
    rows: list[Sample] = []
    with open(path, 'r', encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle)
        required = {'question', 'expected_answer'}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f'CSV is missing required columns: {sorted(missing)}')
        for row in reader:
            rows.append(Sample(question=(row.get('question') or '').strip(), expected_answer=(row.get('expected_answer') or '').strip()))
    return rows

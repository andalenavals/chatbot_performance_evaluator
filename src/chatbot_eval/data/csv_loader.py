from __future__ import annotations

import csv
from pathlib import Path
from typing import List

from .models import EvalSample

REQUIRED_COLUMNS = {"question", "expected_answer"}


def load_samples_from_csv(path: str | Path) -> List[EvalSample]:
    csv_path = Path(path)
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS - headers
        if missing:
            raise ValueError(f"CSV file is missing required columns: {sorted(missing)}")

        rows: List[EvalSample] = []
        for index, row in enumerate(reader, start=1):
            question = (row.get("question") or "").strip()
            expected = (row.get("expected_answer") or "").strip()
            if not question:
                continue
            row_id = row.get("row_id") or f"row_{index}"
            metadata = {k: v for k, v in row.items() if k not in {"question", "expected_answer", "row_id"}}
            rows.append(EvalSample(question=question, expected_answer=expected, row_id=row_id, metadata=metadata))
    return rows

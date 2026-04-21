from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def list_json_files(path: str | Path) -> list[Path]:
    return sorted(Path(path).glob("*.json"))


def write_jsonl(path: str | Path, rows: Iterable[dict]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

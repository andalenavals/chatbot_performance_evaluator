from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(slots=True)
class EvalSample:
    question: str
    expected_answer: str
    row_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)

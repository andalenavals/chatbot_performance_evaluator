from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class JudgeConfig:
    name: str
    model_config: str
    prompt_path: str
    debug: bool = False

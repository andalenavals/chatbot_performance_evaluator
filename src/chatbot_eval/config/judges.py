from __future__ import annotations

"""Configuration model for LLM-as-a-judge metrics."""

from dataclasses import dataclass


@dataclass(slots=True)
class JudgeConfig:
    """One judge metric configuration entry."""

    name: str
    model_config: str
    prompt_path: str
    debug: bool = False

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from chatbot_eval.utils.templating import render_template

from .base import MetricResult

_JSON_PATTERN = re.compile(r"\{.*\}", re.DOTALL)
_NUMBER_PATTERN = re.compile(r"-?\d+(?:\.\d+)?")


@dataclass(slots=True)
class LLMJudgeMetric:
    name: str
    judge_client: Any
    prompt_path: Path
    score_range: tuple[float, float] = (1.0, 5.0)
    debug: bool = False
    judge_model_name: str = "unknown"

    def score(self, sample, bot_result) -> MetricResult:
        prompt = render_template(
            self.prompt_path,
            question=sample.question,
            expected_answer=sample.expected_answer,
            generated_answer=bot_result.answer,
        )
        completion = self.judge_client.generate(prompt)
        parsed = self._parse_judge_output(completion.text)
        score = max(self.score_range[0], min(self.score_range[1], parsed.get("score", self.score_range[0])))
        details = {
            "judge_model": self.judge_model_name,
            "reason": parsed.get("reason", ""),
        }
        if self.debug:
            details["debug"] = {
                "raw_output": completion.raw,
                "text_output": completion.text,
                "thinking": completion.thinking,
                "prompt_path": str(self.prompt_path),
            }
        return MetricResult(name=self.name, score=float(score), details=details)

    def _parse_judge_output(self, text: str) -> dict[str, Any]:
        match = _JSON_PATTERN.search(text)
        if match:
            try:
                data = json.loads(match.group(0))
                return {
                    "score": float(data.get("score", self.score_range[0])),
                    "reason": str(data.get("reason", "")),
                }
            except json.JSONDecodeError:
                pass
        number_match = _NUMBER_PATTERN.search(text)
        score = float(number_match.group(0)) if number_match else self.score_range[0]
        return {"score": score, "reason": text.strip()}

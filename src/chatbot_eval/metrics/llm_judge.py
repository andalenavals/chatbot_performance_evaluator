from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from chatbot_eval.types import BotResult, MetricResult, Sample
from chatbot_eval.utils.files import render_template


@dataclass(slots=True)
class LLMJudgeMetric:
    name: str
    llm_client: object
    prompt_path: str | Path
    debug: bool = False

    def score(self, sample: Sample, bot_result: BotResult) -> MetricResult:
        prompt = render_template(self.prompt_path, question=sample.question, expected_answer=sample.expected_answer, generated_answer=bot_result.answer)
        completion = self.llm_client.generate(prompt)
        parsed = self._parse_json(completion.text)
        details = {'reason': parsed.get('reason', '')}
        if self.debug:
            details['judge_output'] = completion.text
            if completion.thinking:
                details['judge_thinking'] = completion.thinking
        return MetricResult(name=self.name, score=float(parsed.get('score', 0.0)), details=details)

    def _parse_json(self, text: str) -> dict:
        text = text.strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            match = re.search(r'\{.*\}', text, flags=re.DOTALL)
            if match:
                return json.loads(match.group(0))
            return {'score': 0.0, 'reason': 'Judge output was not valid JSON.'}

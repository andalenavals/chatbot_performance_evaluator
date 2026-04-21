from pathlib import Path

from chatbot_eval.data.models import EvalSample
from chatbot_eval.metrics.llm_judge import LLMJudgeMetric
from chatbot_eval.bots.base import BotResult
from chatbot_eval.clients.base import ChatCompletion


class FakeJudge:
    def generate(self, prompt: str, *, system_prompt=None):
        return ChatCompletion(text='{"score": 4, "reason": "Good"}', thinking="trace", raw={"ok": True})


def test_judge_metric_parses_json_and_debug(tmp_path: Path) -> None:
    prompt = tmp_path / "judge.txt"
    prompt.write_text("Question: $question\nExpected: $expected_answer\nGenerated: $generated_answer", encoding="utf-8")
    metric = LLMJudgeMetric(
        name="judge_test",
        judge_client=FakeJudge(),
        prompt_path=prompt,
        debug=True,
        judge_model_name="deepseek-r1",
    )
    result = metric.score(EvalSample(question="Q", expected_answer="A", row_id="1"), BotResult(answer="A", latency_ms=1.2))
    assert result.score == 4
    assert result.details["judge_model"] == "deepseek-r1"
    assert result.details["debug"]["thinking"] == "trace"

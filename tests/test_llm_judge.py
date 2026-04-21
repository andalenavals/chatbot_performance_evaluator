from pathlib import Path

from chatbot_eval.metrics.llm_judge import LLMJudgeMetric
from chatbot_eval.types import BotResult, Completion, Sample


class FakeJudge:
    def generate(self, prompt: str):
        return Completion(text='{"score": 4, "reason": "Looks good"}', thinking='trace')


def test_llm_judge_includes_debug_when_enabled(project_root=Path(__file__).resolve().parents[1]):
    metric = LLMJudgeMetric(name='judge', llm_client=FakeJudge(), prompt_path=project_root / 'configs' / 'judges' / 'prompts' / 'relevance_faithfulness.txt', debug=True)
    result = metric.score(Sample(question='Q', expected_answer='A'), BotResult(answer='A'))
    assert result.score == 4
    assert 'judge_output' in result.details
    assert 'judge_thinking' in result.details

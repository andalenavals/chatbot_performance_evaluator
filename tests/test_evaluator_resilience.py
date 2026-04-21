from chatbot_eval.evaluation.evaluator import Evaluator
from chatbot_eval.types import MetricResult, Sample


class BrokenBot:
    name = 'broken'

    def answer(self, question: str):
        raise RuntimeError('boom')


class NoopMetric:
    name = 'noop'

    def score(self, sample, bot_result):
        return MetricResult(name='noop', score=1.0)


def test_evaluator_records_bot_error():
    evaluator = Evaluator(metrics=[NoopMetric()])
    row = evaluator.evaluate_sample(Sample(question='q', expected_answer='a'), BrokenBot())
    assert row['generated_answer'] == ''
    assert 'boom' in row['bot_metadata_json']

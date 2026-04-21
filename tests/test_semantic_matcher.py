from chatbot_eval.data.models import EvalSample
from chatbot_eval.retrieval.semantic_matcher import SemanticMatcher


class FakeEmbeddingClient:
    def embed_texts(self, texts):
        mapping = {
            "reset password": [1.0, 0.0],
            "change password": [0.95, 0.05],
            "premium support": [0.0, 1.0],
        }
        return [mapping[text] for text in texts]


def test_semantic_matcher_returns_best_sample() -> None:
    samples = [
        EvalSample(question="reset password", expected_answer="Use settings", row_id="1"),
        EvalSample(question="premium support", expected_answer="Weekdays", row_id="2"),
    ]
    matcher = SemanticMatcher(FakeEmbeddingClient(), samples)
    match = matcher.best_match("change password")
    assert match.sample.row_id == "1"

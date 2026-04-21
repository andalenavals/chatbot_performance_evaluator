from pathlib import Path

from chatbot_eval.bots.semantic_match import StrictSemanticMatchBot


def test_semantic_match_returns_expected_answer(project_root=Path(__file__).resolve().parents[1]):
    bot = StrictSemanticMatchBot(name='semantic', faq_csv_path=project_root / 'data' / 'faq.csv')
    result = bot.answer('How do I reset my password?')
    assert 'password reset' in result.answer.lower() or 'profile settings' in result.answer.lower()

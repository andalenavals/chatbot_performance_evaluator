from pathlib import Path

from chatbot_eval.io.csv_loader import load_samples_from_csv


def test_load_samples_from_csv(project_root=Path(__file__).resolve().parents[1]):
    rows = load_samples_from_csv(project_root / 'data' / 'faq.csv')
    assert rows
    assert rows[0].question
    assert rows[0].expected_answer

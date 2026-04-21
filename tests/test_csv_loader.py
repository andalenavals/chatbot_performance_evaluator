from pathlib import Path

from chatbot_eval.data.csv_loader import load_samples_from_csv


def test_load_samples_from_csv_reads_required_columns(tmp_path: Path) -> None:
    path = tmp_path / "samples.csv"
    path.write_text("question,expected_answer\nHi,Hello\n", encoding="utf-8")
    samples = load_samples_from_csv(path)
    assert len(samples) == 1
    assert samples[0].question == "Hi"
    assert samples[0].expected_answer == "Hello"

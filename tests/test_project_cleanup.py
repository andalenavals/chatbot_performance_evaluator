from pathlib import Path


def test_no_rag_files_left() -> None:
    root = Path(__file__).resolve().parents[1] / "src" / "chatbot_eval"
    names = {path.name for path in root.rglob("*")}
    assert "rag_chatbot.py" not in names
    assert "domain_rag.py" not in names
    assert "rag_semantic_match.py" not in names

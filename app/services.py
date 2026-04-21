from __future__ import annotations

import hashlib
import tempfile
from pathlib import Path

from chatbot_eval.config.builders import build_bot_from_config
from chatbot_eval.config.loader import load_bot_config
from chatbot_eval.data.csv_loader import load_samples_from_csv
from chatbot_eval.utils.files import list_json_files


def list_bot_configs(config_dir: str | Path) -> list[Path]:
    return list_json_files(config_dir)


def list_csv_files(data_dir: str | Path) -> list[Path]:
    return sorted(Path(data_dir).glob("*.csv"))


def list_text_files(data_dir: str | Path) -> list[Path]:
    return sorted(
        [path for path in Path(data_dir).glob("*") if path.suffix.lower() in {".txt", ".md"}]
    )


def materialize_upload(uploaded_file, suffix: str) -> Path | None:
    if uploaded_file is None:
        return None
    digest = hashlib.sha1(uploaded_file.getvalue()).hexdigest()[:12]
    base = Path(tempfile.gettempdir()) / "chatbot_eval_visual"
    base.mkdir(parents=True, exist_ok=True)
    target = base / f"{digest}{suffix}"
    target.write_bytes(uploaded_file.getvalue())
    return target


def build_bot_with_runtime_files(
    config_path: str | Path,
    *,
    faq_csv_path: str | Path | None = None,
    domain_knowledge_path: str | Path | None = None,
):
    bot_config = load_bot_config(config_path)
    if faq_csv_path is not None and bot_config.bot_type == "strict_semantic_match":
        bot_config.dataset_path = Path(faq_csv_path).resolve()
    if domain_knowledge_path is not None and bot_config.bot_type == "full_context":
        bot_config.domain_knowledge_path = Path(domain_knowledge_path).resolve()
    return build_bot_from_config(bot_config)


def load_samples_for_app(path: str | Path):
    return load_samples_from_csv(path)

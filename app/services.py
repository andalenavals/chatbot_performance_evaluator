from __future__ import annotations

import tempfile
from pathlib import Path

from chatbot_eval.config.runtime import build_bot_from_config
from chatbot_eval.io.csv_loader import load_samples_from_csv


def list_bot_configs(config_dir: Path) -> list[Path]:
    return sorted(config_dir.glob('*.json'))


def list_csv_files(data_dir: Path) -> list[Path]:
    return sorted(data_dir.glob('*.csv'))


def list_text_files(data_dir: Path) -> list[Path]:
    return sorted(data_dir.glob('*.txt'))


def _persist_upload(upload, suffix: str) -> Path | None:
    if upload is None:
        return None
    tmp_dir = Path(tempfile.mkdtemp(prefix='chatbot_eval_'))
    path = tmp_dir / f'upload{suffix}'
    path.write_bytes(upload.getvalue())
    return path


def select_runtime_file(selected_path: Path | None, uploaded_file, suffix: str) -> Path:
    persisted = _persist_upload(uploaded_file, suffix)
    if persisted:
        return persisted
    if selected_path is None:
        raise ValueError(f'Missing required file with suffix {suffix}')
    return selected_path


def build_bot_with_runtime_files(project_root: Path, bot_config_path: Path, faq_csv_path: Path | None, domain_knowledge_path: Path | None, uploaded_csv=None, uploaded_domain=None):
    faq_path = select_runtime_file(faq_csv_path, uploaded_csv, '.csv')
    domain_path = select_runtime_file(domain_knowledge_path, uploaded_domain, '.txt')
    return build_bot_from_config(project_root, bot_config_path, faq_path, domain_path)


def load_samples_for_preview(faq_csv_path: Path | None, uploaded_csv=None):
    faq_path = select_runtime_file(faq_csv_path, uploaded_csv, '.csv')
    return load_samples_from_csv(faq_path)

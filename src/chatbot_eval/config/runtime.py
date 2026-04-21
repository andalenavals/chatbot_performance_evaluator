from __future__ import annotations

"""Runtime helpers to construct bots from the file-system layout."""

from pathlib import Path

from chatbot_eval.bots.factory import BotFactory


def build_bot_from_config(
    project_root: str | Path,
    bot_config_path: str | Path,
    faq_csv_path: str | Path,
    domain_knowledge_path: str | Path,
):
    """Build a bot instance from config and runtime data files."""

    return BotFactory.from_config(
        Path(project_root),
        Path(bot_config_path),
        Path(faq_csv_path),
        Path(domain_knowledge_path),
    )

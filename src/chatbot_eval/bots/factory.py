from __future__ import annotations

from pathlib import Path

from chatbot_eval.bots.full_context import FullContextBot
from chatbot_eval.bots.semantic_match import StrictSemanticMatchBot
from chatbot_eval.config.builders import build_chat_client, load_model_config
from chatbot_eval.utils.files import load_json


class BotFactory:
    @staticmethod
    def from_config(project_root: Path, bot_config_path: Path, faq_csv_path: Path, domain_knowledge_path: Path):
        config = load_json(bot_config_path)
        bot_type = config['type']
        if bot_type == 'strict_semantic_match':
            return StrictSemanticMatchBot(name=config['name'], faq_csv_path=faq_csv_path)
        if bot_type == 'full_context':
            model_cfg = load_model_config(project_root / config['model_config'])
            chat_client = build_chat_client(model_cfg)
            return FullContextBot(name=config['name'], chat_client=chat_client, prompt_path=project_root / config['prompt_path'], domain_knowledge_path=domain_knowledge_path)
        raise ValueError(f'Unsupported bot type: {bot_type}')

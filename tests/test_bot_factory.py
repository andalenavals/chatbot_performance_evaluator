from pathlib import Path

from chatbot_eval.bots.factory import build_bot
from chatbot_eval.config.loader import load_bot_config
from chatbot_eval.config.schema import ModelConfig


class FakeChatClient:
    def generate(self, prompt: str, *, system_prompt=None):
        from chatbot_eval.clients.base import ChatCompletion
        return ChatCompletion(text="ok")


class FakeEmbeddingClient:
    def embed_texts(self, texts):
        return [[1.0, 0.0] for _ in texts]


def test_build_full_context_bot(tmp_path: Path) -> None:
    configs = tmp_path / "configs"
    (configs / "bots").mkdir(parents=True)
    (configs / "models").mkdir(parents=True)

    prompt = configs / "prompt.txt"
    prompt.write_text("$question\n$domain_knowledge", encoding="utf-8")
    knowledge = tmp_path / "knowledge.txt"
    knowledge.write_text("facts", encoding="utf-8")
    bot_cfg = configs / "bots" / "b.json"
    bot_cfg.write_text(
        '{"name":"bot","bot_type":"full_context","chat_model_config":"models/x.json","prompt_path":"prompt.txt","domain_knowledge_path":"../knowledge.txt"}',
        encoding="utf-8",
    )
    config = load_bot_config(bot_cfg)
    bot = build_bot(config, lambda _: ModelConfig(name="x", provider="ollama", model_name="x"), lambda _: FakeChatClient(), lambda _: FakeEmbeddingClient())
    assert bot.name == "bot"

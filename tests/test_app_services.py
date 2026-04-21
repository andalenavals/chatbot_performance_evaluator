from pathlib import Path

from chatbot_eval.config.loader import load_bot_config


def test_runtime_bot_overrides_domain_knowledge(tmp_path: Path) -> None:
    configs = tmp_path / "configs"
    (configs / "bots").mkdir(parents=True)
    (configs / "models").mkdir(parents=True)

    prompt_path = configs / "prompt.txt"
    prompt_path.write_text("$question\n$domain_knowledge", encoding="utf-8")
    knowledge_path = tmp_path / "knowledge.txt"
    knowledge_path.write_text("facts", encoding="utf-8")
    override_knowledge = tmp_path / "override.txt"
    override_knowledge.write_text("override", encoding="utf-8")

    model_cfg = configs / "models" / "x.json"
    model_cfg.write_text(
        '{"name":"x","provider":"ollama","model_name":"x"}',
        encoding="utf-8",
    )
    bot_cfg = configs / "bots" / "b.json"
    bot_cfg.write_text(
        '{"name":"bot","bot_type":"full_context","chat_model_config":"models/x.json","prompt_path":"prompt.txt","domain_knowledge_path":"../knowledge.txt"}',
        encoding="utf-8",
    )

    bot_config = load_bot_config(bot_cfg)
    bot_config.domain_knowledge_path = override_knowledge
    assert bot_config.domain_knowledge_path == override_knowledge

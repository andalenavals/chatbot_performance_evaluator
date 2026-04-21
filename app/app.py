from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

from chatbot_eval.config.builders import build_bot_from_config
from chatbot_eval.data.csv_loader import load_samples_from_csv
from chatbot_eval.evaluation.evaluator import Evaluator
from chatbot_eval.metrics.registry import build_default_metrics
from chatbot_eval.utils.files import list_json_files

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOT_CONFIG_DIR = PROJECT_ROOT / "configs" / "bots"
DATASET_PATH = PROJECT_ROOT / "data" / "sample_eval.csv"


@st.cache_resource(show_spinner=False)
def load_bot(config_path: str):
    return build_bot_from_config(config_path)


@st.cache_data(show_spinner=False)
def load_samples(path: str):
    return load_samples_from_csv(path)


@st.cache_resource(show_spinner=False)
def load_evaluator(root: str):
    return Evaluator(metrics=build_default_metrics(Path(root)))


def main() -> None:
    st.set_page_config(page_title="Chatbot Evaluator", layout="wide")
    st.title("Chatbot Evaluator")

    bot_configs = list_json_files(BOT_CONFIG_DIR)
    selected_path = st.sidebar.selectbox("Bot config", bot_configs, format_func=lambda p: p.stem)
    show_thinking = st.sidebar.toggle("Show thought/debug details", value=False)

    try:
        bot = load_bot(str(selected_path))
    except RuntimeError as exc:
        st.error(f"This bot config is not currently available: {exc}")
        st.stop()

    samples = load_samples(str(DATASET_PATH))
    evaluator = load_evaluator(str(PROJECT_ROOT))

    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader("Chat with bot")
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["text"])
                if show_thinking and message.get("debug"):
                    with st.expander("Debug details"):
                        st.json(message["debug"])

        user_input = st.chat_input("Ask something")
        if user_input:
            result = bot.answer(user_input)
            st.session_state.messages.append({"role": "user", "text": user_input})
            bot_debug = {
                "thinking": result.metadata.get("thinking"),
                "raw_response": result.metadata.get("raw_response"),
                "metadata": result.metadata,
            }
            st.session_state.messages.append({"role": "assistant", "text": result.answer, "debug": bot_debug})
            st.rerun()

    with right_col:
        st.subheader("Inspect a benchmark sample")
        sample_options = {f"{sample.row_id}: {sample.question}": sample for sample in samples}
        sample_label = st.selectbox("Sample question", list(sample_options))
        selected_sample = sample_options[sample_label]

        row = evaluator.evaluate_sample(selected_sample, bot)
        st.markdown("**Expected answer**")
        st.write(row["expected_answer"])
        st.markdown("**Generated answer**")
        st.write(row["generated_answer"])

        metrics_df = pd.DataFrame(
            [{"metric": name, "score": score} for name, score in row["metrics"].items()]
        )
        st.markdown("**Metric values**")
        st.dataframe(metrics_df, use_container_width=True, hide_index=True)

        st.markdown("**Bot metadata**")
        st.json(row["bot_metadata"])

        st.markdown("**Metric details**")
        for metric_name, details in row["metric_details"].items():
            with st.expander(metric_name, expanded=False):
                visible_details = details
                if not show_thinking and isinstance(details, dict) and "debug" in details:
                    visible_details = {k: v for k, v in details.items() if k != "debug"}
                st.json(visible_details)

        st.markdown("**Selected bot config**")
        st.code(Path(selected_path).read_text(encoding="utf-8"), language="json")


if __name__ == "__main__":
    main()

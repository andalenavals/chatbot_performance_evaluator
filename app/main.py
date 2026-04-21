from __future__ import annotations

"""Streamlit application for chatting with bots and inspecting evaluation rows."""

import json
from pathlib import Path

import streamlit as st

from app.services import (
    build_bot_with_runtime_files,
    list_bot_configs,
    list_csv_files,
    list_text_files,
    load_samples_for_preview,
)
from chatbot_eval.evaluation.evaluator import Evaluator
from chatbot_eval.metrics.registry import build_default_metrics

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_BOTS = PROJECT_ROOT / 'configs' / 'bots'
DATA_DIR = PROJECT_ROOT / 'data'


@st.cache_data(show_spinner=False)
def get_bot_configs() -> list[Path]:
    return list_bot_configs(CONFIG_BOTS)


@st.cache_data(show_spinner=False)
def get_csv_files() -> list[Path]:
    return list_csv_files(DATA_DIR)


@st.cache_data(show_spinner=False)
def get_text_files() -> list[Path]:
    return list_text_files(DATA_DIR)


def main() -> None:
    """Run the Streamlit application."""

    st.set_page_config(layout='wide', page_title='Chatbot Evaluator')
    st.title('Chatbot Evaluator')
    st.caption('Benchmark full-context and strict semantic-match chatbot variants against FAQ datasets.')

    bot_configs = get_bot_configs()
    csv_files = get_csv_files()
    text_files = get_text_files()

    with st.sidebar:
        st.header('Configuration')
        selected_bot = st.selectbox('Bot config', bot_configs, format_func=lambda p: p.name)
        selected_csv = st.selectbox('FAQ CSV', csv_files, format_func=lambda p: p.name)
        selected_domain = st.selectbox('Domain knowledge', text_files, format_func=lambda p: p.name)
        uploaded_csv = st.file_uploader('Or upload FAQ CSV', type=['csv'])
        uploaded_domain = st.file_uploader('Or upload domain knowledge', type=['txt'])
        show_debug = st.checkbox('Show thought process / debug', value=False)

    left, right = st.columns(2)

    with left:
        st.subheader('Chat')
        question = st.text_area('Ask the bot something', height=120)
        if st.button('Send', use_container_width=True) and question.strip():
            try:
                bot = build_bot_with_runtime_files(
                    PROJECT_ROOT,
                    selected_bot,
                    selected_csv,
                    selected_domain,
                    uploaded_csv,
                    uploaded_domain,
                )
                result = bot.answer(question.strip())
                st.markdown('**Answer**')
                st.write(result.answer)
                if show_debug:
                    st.markdown('**Bot metadata**')
                    st.json(result.metadata)
            except Exception as exc:  # pragma: no cover - UI guard
                st.error(str(exc))

    with right:
        st.subheader('Benchmark inspector')
        try:
            samples = load_samples_for_preview(selected_csv, uploaded_csv)
            if not samples:
                st.info('No samples available.')
                return
            idx = st.selectbox('Select sample question', list(range(len(samples))), format_func=lambda i: samples[i].question)
            sample = samples[idx]
            st.markdown('**Question**')
            st.write(sample.question)
            st.markdown('**Expected answer**')
            st.write(sample.expected_answer)

            bot = build_bot_with_runtime_files(
                PROJECT_ROOT,
                selected_bot,
                selected_csv,
                selected_domain,
                uploaded_csv,
                uploaded_domain,
            )
            metrics = build_default_metrics(PROJECT_ROOT)
            evaluator = Evaluator(metrics=metrics)
            row = evaluator.evaluate_sample(sample, bot)

            st.markdown('**Generated answer**')
            st.write(row['generated_answer'])
            st.markdown('**Metric values**')
            st.json(json.loads(row['metrics_json']))
            if show_debug:
                st.markdown('**Metric details**')
                st.json(json.loads(row['metric_details_json']))
                st.markdown('**Bot metadata**')
                st.json(json.loads(row['bot_metadata_json']))
        except Exception as exc:  # pragma: no cover - UI guard
            st.error(str(exc))


if __name__ == '__main__':
    main()

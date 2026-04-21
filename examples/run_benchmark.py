from __future__ import annotations

import argparse
from pathlib import Path

from chatbot_eval.config.runtime import build_bot_from_config
from chatbot_eval.evaluation.evaluator import Evaluator
from chatbot_eval.io.csv_loader import load_samples_from_csv
from chatbot_eval.io.reporting import summarize_by_bot, write_rows_csv, write_rows_jsonl
from chatbot_eval.metrics.registry import build_default_metrics


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument('--faq-csv', default=str(project_root / 'data' / 'faq.csv'))
    parser.add_argument('--domain-knowledge', default=str(project_root / 'data' / 'domain_knowledge.txt'))
    parser.add_argument('--output-dir', default=str(project_root / 'outputs'))
    args = parser.parse_args()

    samples = load_samples_from_csv(args.faq_csv)
    bots = []
    for bot_cfg in sorted((project_root / 'configs' / 'bots').glob('*.json')):
        try:
            bots.append(build_bot_from_config(project_root, bot_cfg, args.faq_csv, args.domain_knowledge))
        except Exception as exc:
            print(f'Skipping {bot_cfg.name}: {exc}')
    if not bots:
        raise RuntimeError('No bots could be constructed. Check your configs.')

    evaluator = Evaluator(metrics=build_default_metrics(project_root))
    rows = evaluator.evaluate_dataset(samples=samples, bots=bots)
    output_dir = Path(args.output_dir)
    write_rows_csv(rows, output_dir / 'results_detailed.csv')
    write_rows_jsonl(rows, output_dir / 'results_detailed.jsonl')
    write_rows_csv(summarize_by_bot(rows), output_dir / 'summary_by_bot.csv')
    print(f'Wrote outputs to {output_dir}')


if __name__ == '__main__':
    main()

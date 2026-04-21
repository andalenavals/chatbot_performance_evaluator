from pathlib import Path

from app.services import list_bot_configs, list_csv_files, list_text_files


def test_app_lists_files(project_root=Path(__file__).resolve().parents[1]):
    root = project_root
    assert list_bot_configs(root / 'configs' / 'bots')
    assert list_csv_files(root / 'data')
    assert list_text_files(root / 'data')

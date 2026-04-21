from __future__ import annotations

"""Small file-system and templating utilities used across the project."""

import json
import os
from pathlib import Path
from string import Template
from typing import Any


def resolve_env(value: Any) -> Any:
    """Resolve ``${ENV_VAR}`` placeholders recursively in Python objects."""

    if isinstance(value, str) and value.startswith('${') and value.endswith('}'):
        return os.getenv(value[2:-1], '')
    if isinstance(value, dict):
        return {k: resolve_env(v) for k, v in value.items()}
    if isinstance(value, list):
        return [resolve_env(v) for v in value]
    return value


def load_json(path: str | Path) -> dict[str, Any]:
    """Load JSON and resolve environment placeholders."""

    data = json.loads(Path(path).read_text(encoding='utf-8'))
    return resolve_env(data)


def load_text(path: str | Path) -> str:
    """Load text content from disk."""

    return Path(path).read_text(encoding='utf-8')


def render_template(path: str | Path, **kwargs: str) -> str:
    """Render a ``string.Template`` file from disk."""

    template = Template(load_text(path))
    return template.safe_substitute(**kwargs)

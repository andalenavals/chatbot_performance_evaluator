from __future__ import annotations

from pathlib import Path
from string import Template
from typing import Any

from .files import read_text


def render_template(path: str | Path, **values: Any) -> str:
    return Template(read_text(path)).safe_substitute(**values)

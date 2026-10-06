"""Атомарное сохранение проверенного снимка JSON."""

import json
import os
import tempfile
from pathlib import Path

from validation import validate_state


def load_json(path: str | Path) -> dict:
    with Path(path).open(encoding="utf-8") as stream:
        state = json.load(stream)
    validate_state(state)
    return state


def save_json(state: dict, path: str | Path) -> None:
    validate_state(state)
    path = Path(path)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            delete=False,
        ) as stream:
            temporary = Path(stream.name)
            json.dump(state, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)

import json, os
from pathlib import Path
from typing import Any, Dict

def dummy_dir() -> str:
    return os.getenv("DUMMY_DATA_DIR", str(Path.cwd() / "data"))

def load_json(name: str):
    path = Path(dummy_dir()) / name
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

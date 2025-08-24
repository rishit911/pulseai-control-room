import json, os
from pathlib import Path
from typing import Any, Dict

def dummy_dir() -> str:
    # Get the absolute path to MLOps_Engineer4/data directory
    current_file = Path(__file__).resolve()
    # Go up from utils -> app -> MLOps_Engineer4, then into data
    engineer4_data = current_file.parent.parent.parent / "data"
    return os.getenv("DUMMY_DATA_DIR", str(engineer4_data))

def load_json(name: str):
    path = Path(dummy_dir()) / name
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

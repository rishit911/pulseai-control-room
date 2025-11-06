import os
import json
import yaml
from datetime import datetime


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def write_json(path, data):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)


def timestamp():
    return datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%SZ")

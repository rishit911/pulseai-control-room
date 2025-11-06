import json
from .utils import write_json


def emit_contracts(out_dir):
    contract = {
        "artifacts": {
            "validation": "validation.json",
            "drift": "drift.json",
            "fairness": "fairness.json",
            "summary": "summary.json",
        }
    }
    write_json(out_dir + "/contracts.json", contract)
    return contract

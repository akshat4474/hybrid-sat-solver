import os
import csv
import json
from datetime import datetime
from typing import Dict, List, Union

# Ensure the log directory exists
os.makedirs("logs", exist_ok=True)


def log_solver_result(entry: Dict):
    """
    Log a solver run entry to logs/solver_log.csv, dynamically updating fieldnames.
    """
    path = "logs/solver_log.csv"
    is_new = not os.path.exists(path)

    existing_fieldnames = set()
    rows = []

    if not is_new:
        with open(path, "r", newline='') as f:
            reader = csv.DictReader(f)
            existing_fieldnames = set(reader.fieldnames)
            rows = list(reader)

    # Current fields plus timestamp
    log_data = {
        "timestamp": datetime.now().isoformat(),
        **entry
    }
    all_fieldnames = sorted(set(log_data.keys()).union(existing_fieldnames))

    with open(path, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=all_fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        writer.writerow(log_data)


def log_cnf_metadata(entry: Dict):
    """
    Log metadata about a generated CNF to logs/cnf_metadata.csv
    """
    path = "logs/cnf_metadata.csv"
    is_new = not os.path.exists(path)
    fields = ["timestamp", "filename", "num_vars", "num_clauses", "ratio", "seed"]

    with open(path, "a", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        if is_new:
            writer.writeheader()
        writer.writerow({
            **{
                "timestamp": datetime.now().isoformat()
            },
            **entry
        })


def write_json(path: str, data: Union[Dict, List]):
    """
    Save structured data to a JSON file.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def read_json(path: str) -> Union[Dict, List]:
    """
    Load JSON data from file.
    """
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

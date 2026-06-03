from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def parse_float(value: str | None) -> float | None:
    if value is None or value.strip() == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def parse_date(value: str | None) -> str | None:
    if value is None or value.strip() == "":
        return None
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(value, fmt).date().isoformat()
        except ValueError:
            continue
    return value


def load_csv_rows(file_name: str) -> list[dict[str, Any]]:
    path = DATA_DIR / file_name
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows: list[dict[str, Any]] = []
        for row in reader:
            rows.append({
                "date": parse_date(row.get("date")),
                "category": row.get("category", "") or "Unknown",
                "region": row.get("region", "") or "Unknown",
                "value": parse_float(row.get("value")),
                "latitude": parse_float(row.get("latitude")),
                "longitude": parse_float(row.get("longitude")),
                "note": row.get("note", "") or "",
            })
        return rows


def load_data() -> list[dict[str, Any]]:
    return load_csv_rows("sample_data.csv")


def load_logs() -> list[dict[str, Any]]:
    path = DATA_DIR / "sample_logs.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return [
            {
                "timestamp": row.get("timestamp", ""),
                "level": row.get("level", "INFO"),
                "source": row.get("source", "system"),
                "message": row.get("message", ""),
            }
            for row in reader
        ]

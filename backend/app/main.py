from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .csv_data import load_data, load_logs

app = FastAPI(title="CSV Dashboard API")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://dashboard-cl0jm71jd-ado62s-projects.vercel.app",
    "https://dashboard-app-phi-beryl.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA = load_data()
LOGS = load_logs()


@app.get("/")
async def root() -> dict[str, str]:
    return {"status": "ready", "message": "Python CSV dashboard backend is running."}


@app.get("/api/data/overview")
async def get_overview() -> dict[str, Any]:
    total_rows = len(DATA)
    categories = Counter(item["category"] for item in DATA)
    regions = Counter(item["region"] for item in DATA)
    values = [item["value"] for item in DATA if item["value"] is not None]
    return {
        "totalRows": total_rows,
        "categories": categories,
        "regions": regions,
        "valueMin": min(values) if values else None,
        "valueMax": max(values) if values else None,
        "valueAverage": round(sum(values) / len(values), 2) if values else None,
        "latestRecords": DATA[-5:],
    }


@app.get("/api/data/chart")
async def get_chart() -> dict[str, Any]:
    series: dict[str, float] = defaultdict(float)
    for item in DATA:
        if item["date"] and item["value"] is not None:
            series[item["date"]] += item["value"]
    return {
        "series": [
            {"date": date, "value": total}
            for date, total in sorted(series.items())
        ]
    }


@app.get("/api/data/table")
async def get_table(limit: int = 50) -> dict[str, Any]:
    return {
        "rows": DATA[:limit],
        "count": len(DATA),
    }


@app.get("/api/data/locations")
async def get_locations() -> dict[str, Any]:
    points = [
        {
            "region": item["region"],
            "category": item["category"],
            "value": item["value"],
            "latitude": item["latitude"],
            "longitude": item["longitude"],
            "note": item["note"],
        }
        for item in DATA
        if item["latitude"] is not None and item["longitude"] is not None
    ]
    return {"points": points}


@app.get("/api/logs")
async def get_logs(limit: int = 50) -> dict[str, Any]:
    return {"logs": LOGS[:limit], "count": len(LOGS)}

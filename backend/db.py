from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def init_db(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                input_name TEXT,
                input_path TEXT,
                input_size INTEGER,
                output_format TEXT,
                output_path TEXT,
                output_size INTEGER,
                status TEXT,
                options TEXT,
                created_at TEXT,
                updated_at TEXT,
                error TEXT
            )
            """
        )
        conn.commit()


def create_job(db_path: Path, payload: dict) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO jobs (
                id, type, input_name, input_path, input_size,
                output_format, output_path, output_size, status,
                options, created_at, updated_at, error
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload["id"],
                payload["type"],
                payload.get("input_name"),
                payload.get("input_path"),
                payload.get("input_size"),
                payload.get("output_format"),
                payload.get("output_path"),
                payload.get("output_size"),
                payload.get("status"),
                json.dumps(payload.get("options", {}), ensure_ascii=False),
                payload.get("created_at"),
                payload.get("updated_at"),
                payload.get("error"),
            ),
        )
        conn.commit()


def update_job(db_path: Path, job_id: str, updates: dict) -> None:
    if not updates:
        return
    updates["updated_at"] = updates.get("updated_at") or utc_now()
    columns = ", ".join([f"{key} = ?" for key in updates])
    values = [json.dumps(value, ensure_ascii=False) if key == "options" else value for key, value in updates.items()]
    with sqlite3.connect(db_path) as conn:
        conn.execute(f"UPDATE jobs SET {columns} WHERE id = ?", [*values, job_id])
        conn.commit()


def fetch_job(db_path: Path, job_id: str) -> dict | None:
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
        if not row:
            return None
        payload = dict(row)
        payload["options"] = json.loads(payload.get("options") or "{}")
        return payload

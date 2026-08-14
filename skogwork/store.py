"""Session index.

The SDK/CLI already owns the transcripts. This only records which session id
belongs to which project directory, so `--continue` and `skogwork sessions`
work without shelling out to the CLI.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import asdict, dataclass
from pathlib import Path

STATE_DIR = Path(
    os.environ.get("XDG_STATE_HOME", Path.home() / ".local" / "state")
) / "skogwork"
INDEX = STATE_DIR / "sessions.json"


@dataclass
class Entry:
    session_id: str
    cwd: str
    started_at: float
    updated_at: float
    turns: int = 0
    title: str = ""


def _load() -> list[dict]:
    if not INDEX.is_file():
        return []
    try:
        return json.loads(INDEX.read_text())
    except json.JSONDecodeError:
        return []


def _save(rows: list[dict]) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    tmp = INDEX.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(rows, indent=2))
    tmp.replace(INDEX)


def record(entry: Entry) -> None:
    rows = [r for r in _load() if r.get("session_id") != entry.session_id]
    rows.append(asdict(entry))
    rows.sort(key=lambda r: r.get("updated_at", 0), reverse=True)
    _save(rows[:500])


def latest_for(cwd: Path) -> Entry | None:
    target = str(cwd.resolve())
    for row in _load():
        if row.get("cwd") == target:
            return Entry(**row)
    return None


def list_all(cwd: Path | None = None, limit: int = 20) -> list[Entry]:
    rows = _load()
    if cwd is not None:
        target = str(cwd.resolve())
        rows = [r for r in rows if r.get("cwd") == target]
    return [Entry(**r) for r in rows[:limit]]


def new_entry(session_id: str, cwd: Path, title: str = "") -> Entry:
    now = time.time()
    return Entry(
        session_id=session_id,
        cwd=str(cwd.resolve()),
        started_at=now,
        updated_at=now,
        title=title[:120],
    )

"""Session index.

The SDK/CLI already owns the transcripts. This only records which session id
belongs to which project directory, so `--continue` and `skogwork sessions`
work without shelling out to the CLI.

An index we cannot parse is renamed aside and reported rather than treated as
empty, so a later write cannot quietly discard entries we simply failed to read.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import asdict, dataclass
from pathlib import Path

from skogwork.render import console

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


def _quarantine(reason: str) -> None:
    """Move a damaged index aside so the next write cannot silently replace it."""
    stamp = time.strftime("%Y%m%d-%H%M%S")
    backup = INDEX.with_name(f"sessions.corrupt-{stamp}.json")
    nth = 1
    while backup.exists():  # never overwrite an earlier preserved copy
        backup = INDEX.with_name(f"sessions.corrupt-{stamp}.{nth}.json")
        nth += 1
    try:
        INDEX.replace(backup)
    except OSError as exc:
        console.print(
            f"[red]session index unreadable[/red] ({reason}); "
            f"could not set it aside: {exc}"
        )
        return
    console.print(
        f"[yellow]session index unreadable[/yellow] ({reason}); "
        f"kept it at [dim]{backup}[/dim] and started a new one."
    )


def _load() -> list[dict]:
    if not INDEX.is_file():
        return []
    try:
        rows = json.loads(INDEX.read_text())
    except (json.JSONDecodeError, OSError) as exc:
        _quarantine(str(exc))
        return []
    if not isinstance(rows, list):
        _quarantine(f"expected a list, got {type(rows).__name__}")
        return []
    return [r for r in rows if isinstance(r, dict)]


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

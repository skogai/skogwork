#!/usr/bin/env python3
"""Create and perform basic checks on SkogAI architecture records."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
ROOT = SKILL_DIR.parents[2]
REQUIRED_SECTIONS = {
    "feature": ("outcome", "scenarios", "verification"),
    "decision": ("context", "options", "decision", "consequences"),
}


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not slug:
        raise ValueError("title must contain a letter or number")
    return slug


def create(kind: str, title: str) -> Path:
    template = (SKILL_DIR / "assets" / f"{kind}.md").read_text()
    slug = slugify(title)
    if kind == "feature":
        target = ROOT / "docs" / "features" / f"{slug}.md"
    else:
        target = ROOT / "docs" / "decisions" / f"{date.today().isoformat()}-{slug}.md"
    if target.exists():
        raise FileExistsError(f"record already exists: {target.relative_to(ROOT)}")
    target.parent.mkdir(parents=True, exist_ok=True)
    content = template.replace("<title>", title).replace("<date>", date.today().isoformat())
    target.write_text(content)
    return target


def check(path: Path) -> list[str]:
    text = path.read_text()
    errors: list[str] = []
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        errors.append("missing YAML frontmatter")
    if re.search(r"<[^>]+>", text):
        errors.append("unresolved template placeholders")
    headings = {heading.lower() for heading in re.findall(r"^## (.+)$", text, re.MULTILINE)}
    kind = "feature" if "outcome" in headings else "decision"
    for section in REQUIRED_SECTIONS[kind]:
        if section not in headings:
            errors.append(f"missing section: {section}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    new = sub.add_parser("new")
    new.add_argument("kind", choices=REQUIRED_SECTIONS)
    new.add_argument("title")
    verify = sub.add_parser("check")
    verify.add_argument("path", type=Path)
    args = parser.parse_args()

    try:
        if args.command == "new":
            target = create(args.kind, args.title)
            print(target.relative_to(ROOT))
            return 0
        errors = check(args.path)
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"{args.path}: {error}", file=sys.stderr)
        return 1
    print(f"{args.path}: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

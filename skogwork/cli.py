"""skogwork entrypoint."""

from __future__ import annotations

import argparse
import asyncio
import sys
import time
from pathlib import Path

from skogwork import store
from skogwork.config import USER_CONFIG, load
from skogwork.render import StreamRenderer, console


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="skogwork",
        description="Local Cowork-alike on the Claude Agent SDK.",
    )
    p.add_argument("prompt", nargs="*", help="run one turn non-interactively and exit")
    p.add_argument("-C", "--cwd", default=".", help="project directory (default: .)")
    p.add_argument("-c", "--continue", dest="cont", action="store_true",
                   help="resume the most recent session for this directory")
    p.add_argument("-r", "--resume", metavar="ID", help="resume a specific session id")
    p.add_argument("-m", "--model", help="model override")
    p.add_argument("--mode", dest="permission_mode",
                   choices=["default", "acceptEdits", "plan", "bypassPermissions", "dontAsk"],
                   help="permission mode")
    p.add_argument("--skills", help="comma-separated skill names, or 'all' / 'none'")
    p.add_argument("--tools", help="comma-separated allowed tools (replaces defaults)")
    p.add_argument("--budget", type=float, metavar="USD", help="max spend for the session")
    p.add_argument("--sessions", action="store_true", help="list recent sessions and exit")
    p.add_argument("--config", action="store_true", help="print resolved config and exit")
    return p


def _overrides(args: argparse.Namespace) -> dict:
    ov: dict = {"model": args.model, "permission_mode": args.permission_mode,
                "max_budget_usd": args.budget}
    if args.tools:
        ov["allowed_tools"] = [t.strip() for t in args.tools.split(",") if t.strip()]
    if args.skills:
        if args.skills == "none":
            ov["skills"] = []
        elif args.skills == "all":
            ov["skills"] = "all"
        else:
            ov["skills"] = [s.strip() for s in args.skills.split(",") if s.strip()]
    return ov


async def one_shot(cfg, prompt: str, resume: str | None) -> int:
    from claude_agent_sdk import ClaudeAgentOptions, query
    from claude_agent_sdk.types import (
        AssistantMessage,
        ResultMessage,
        StreamEvent,
        SystemMessage,
        UserMessage,
    )

    kwargs = cfg.to_options_kwargs()
    if resume:
        kwargs["resume"] = resume
    renderer = StreamRenderer(streaming=True)
    entry = None
    code = 0

    async for message in query(prompt=prompt, options=ClaudeAgentOptions(**kwargs)):
        if isinstance(message, StreamEvent):
            renderer.stream_event(message.event)
        elif isinstance(message, AssistantMessage):
            renderer.assistant(message)
        elif isinstance(message, UserMessage):
            renderer.tool_result(message)
        elif isinstance(message, SystemMessage):
            if message.subtype == "init":
                sid = (message.data or {}).get("session_id")
                if sid:
                    entry = store.new_entry(sid, cfg.cwd, title=prompt)
            renderer.system(message)
        elif isinstance(message, ResultMessage):
            renderer.result(message)
            code = 1 if message.is_error else 0
            if entry:
                entry.turns = message.num_turns
                entry.cost_usd = message.total_cost_usd or 0.0
                entry.updated_at = time.time()
                store.record(entry)
    return code


def main() -> None:
    args = build_parser().parse_args()
    cwd = Path(args.cwd).expanduser().resolve()
    if not cwd.is_dir():
        console.print(f"[red]not a directory:[/red] {cwd}")
        sys.exit(2)

    if args.sessions:
        rows = store.list_all(None, limit=30)
        if not rows:
            console.print("[dim]no sessions recorded yet[/dim]")
        for e in rows:
            when = time.strftime("%Y-%m-%d %H:%M", time.localtime(e.updated_at))
            console.print(f"[dim]{when}[/dim] {e.session_id[:8]}  [dim]{e.cwd}[/dim]")
            if e.title:
                console.print(f"          {e.title[:80]}")
        return

    cfg = load(cwd, _overrides(args))

    if args.config:
        import json
        console.print(f"[dim]user config: {USER_CONFIG}[/dim]")
        console.print_json(json.dumps(cfg.to_options_kwargs(), default=str))
        return

    resume = args.resume
    if args.cont and not resume:
        latest = store.latest_for(cwd)
        if latest is None:
            console.print("[yellow]no previous session here; starting fresh[/yellow]")
        else:
            resume = latest.session_id

    try:
        if args.prompt:
            sys.exit(asyncio.run(one_shot(cfg, " ".join(args.prompt), resume)))
        from skogwork.repl import run
        run(cfg, resume=resume)
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as exc:  # noqa: BLE001 - top-level friendly failure
        _explain(exc)
        sys.exit(1)


def _explain(exc: Exception) -> None:
    from claude_agent_sdk import CLINotFoundError, ProcessError

    if isinstance(exc, CLINotFoundError):
        console.print(
            "[red]Claude Code CLI not found.[/red]\n"
            "The SDK bundles one; reinstall with [bold]uv tool install --force[/bold], "
            "or point at your own via [bold]cli_path[/bold]."
        )
        return
    text = str(exc)
    if isinstance(exc, ProcessError) or "error result" in text or "auth" in text.lower():
        console.print(f"[red]agent failed:[/red] {text}")
        console.print(
            "[dim]most often auth: run [bold]claude[/bold] once to log in, "
            "or export ANTHROPIC_API_KEY.[/dim]"
        )
        return
    console.print(f"[red]{type(exc).__name__}:[/red] {text}")


if __name__ == "__main__":
    main()

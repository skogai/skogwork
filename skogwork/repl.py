"""Interactive loop."""

from __future__ import annotations

import asyncio
import time
from pathlib import Path
from typing import Any

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.patch_stdout import patch_stdout

from skogwork import store
from skogwork.config import Config
from skogwork.render import StreamRenderer, console

SLASH = [
    "/help",
    "/model",
    "/mode",
    "/mcp",
    "/skills",
    "/tools",
    "/cost",
    "/new",
    "/sessions",
    "/cwd",
    "/quit",
]

HELP = """\
[bold]commands[/bold]
  /model [name]      switch model (blank = default)
  /mode <mode>       default | acceptEdits | plan | bypassPermissions | dontAsk
  /mcp               MCP server status
  /skills            skills loaded this session
  /tools             allowed tools
  /cost              session cost so far
  /new               start a fresh session in this directory
  /sessions          recent sessions for this directory
  /cwd               show working directory
  /quit              exit  (ctrl-d also works)

esc or ctrl-c during a turn interrupts Claude.
"""


class Repl:
    def __init__(self, cfg: Config, resume: str | None = None) -> None:
        self.cfg = cfg
        self.resume = resume
        self.client: Any = None
        self.entry: store.Entry | None = None
        self.session_id: str | None = None
        self.skills: list[str] = []
        self.cost = 0.0
        self.renderer = StreamRenderer(streaming=True)

        hist = store.STATE_DIR / "history"
        store.STATE_DIR.mkdir(parents=True, exist_ok=True)
        self.prompt = PromptSession(
            history=FileHistory(str(hist)),
            completer=WordCompleter(SLASH, sentence=True),
        )

    # -- lifecycle --------------------------------------------------------
    async def start(self) -> None:
        from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient

        kwargs = self.cfg.to_options_kwargs()
        if self.resume:
            kwargs["resume"] = self.resume
        options = ClaudeAgentOptions(**kwargs)
        self.client = ClaudeSDKClient(options=options)
        await self.client.connect()

        info = await self.client.get_server_info() or {}
        self.session_id = info.get("session_id") or info.get("sessionId")
        console.print(
            f"[bold]skogwork[/bold] [dim]{self.cfg.cwd}[/dim]"
            + (f"  [dim]resumed {self.resume[:8]}[/dim]" if self.resume else "")
        )
        console.print("[dim]/help for commands[/dim]\n")

    async def stop(self) -> None:
        if self.client is not None:
            await self.client.disconnect()
        self._persist()

    def _persist(self) -> None:
        if self.entry is None:
            return
        self.entry.updated_at = time.time()
        self.entry.cost_usd = self.cost
        store.record(self.entry)

    # -- main loop --------------------------------------------------------
    async def run(self) -> None:
        await self.start()
        try:
            while True:
                try:
                    with patch_stdout():
                        line = await self.prompt.prompt_async("› ")
                except (EOFError, KeyboardInterrupt):
                    break

                line = line.strip()
                if not line:
                    continue
                if line.startswith("/"):
                    if await self.command(line):
                        break
                    continue

                await self.turn(line)
        finally:
            await self.stop()

    async def turn(self, text: str) -> None:
        from claude_agent_sdk.types import (
            AssistantMessage,
            ResultMessage,
            StreamEvent,
            SystemMessage,
            UserMessage,
        )

        await self.client.query(text)
        try:
            async for message in self.client.receive_response():
                if isinstance(message, StreamEvent):
                    self.renderer.stream_event(message.event)
                elif isinstance(message, AssistantMessage):
                    self.renderer.assistant(message)
                elif isinstance(message, UserMessage):
                    self.renderer.tool_result(message)
                elif isinstance(message, SystemMessage):
                    self._on_system(message, text)
                    self.renderer.system(message)
                elif isinstance(message, ResultMessage):
                    self.cost += message.total_cost_usd or 0.0
                    self.session_id = message.session_id
                    if self.entry:
                        self.entry.turns += message.num_turns
                    self.renderer.result(message)
        except KeyboardInterrupt:
            await self.client.interrupt()
            console.print("\n[yellow]interrupted[/yellow]")
        self._persist()
        console.print()

    def _on_system(self, message: Any, first_prompt: str) -> None:
        if message.subtype != "init":
            return
        data = message.data or {}
        self.skills = list(data.get("skills") or [])
        sid = data.get("session_id") or self.session_id
        if sid and self.entry is None:
            self.entry = store.new_entry(sid, self.cfg.cwd, title=first_prompt)
            self.session_id = sid

    # -- slash commands ---------------------------------------------------
    async def command(self, line: str) -> bool:
        """Returns True when the REPL should exit."""
        parts = line.split(maxsplit=1)
        cmd = parts[0]
        arg = parts[1].strip() if len(parts) > 1 else ""

        if cmd in ("/quit", "/exit", "/q"):
            return True

        if cmd == "/help":
            console.print(HELP)

        elif cmd == "/model":
            await self.client.set_model(arg or None)
            console.print(f"[dim]model → {arg or 'default'}[/dim]")

        elif cmd == "/mode":
            valid = {"default", "acceptEdits", "plan", "bypassPermissions", "dontAsk"}
            if arg not in valid:
                console.print(f"[red]modes:[/red] {', '.join(sorted(valid))}")
            else:
                await self.client.set_permission_mode(arg)
                self.cfg.permission_mode = arg
                console.print(f"[dim]mode → {arg}[/dim]")

        elif cmd == "/mcp":
            status = await self.client.get_mcp_status()
            servers = getattr(status, "servers", None) or status.get("servers", [])
            if not servers:
                console.print("[dim]no mcp servers configured[/dim]")
            for srv in servers:
                name = srv.get("name") if isinstance(srv, dict) else srv.name
                state = srv.get("status") if isinstance(srv, dict) else srv.status
                colour = "green" if state == "connected" else "red"
                console.print(f"  [{colour}]●[/{colour}] {name} [dim]{state}[/dim]")

        elif cmd == "/skills":
            if not self.skills:
                console.print("[dim]no user-invocable skills discovered[/dim]")
            else:
                console.print("  " + "\n  ".join(sorted(self.skills)))

        elif cmd == "/tools":
            console.print("  " + ", ".join(self.cfg.allowed_tools))

        elif cmd == "/cost":
            console.print(f"[dim]${self.cost:.4f} this session[/dim]")

        elif cmd == "/cwd":
            console.print(f"[dim]{self.cfg.cwd}[/dim]")

        elif cmd == "/sessions":
            for e in store.list_all(self.cfg.cwd, limit=10):
                when = time.strftime("%m-%d %H:%M", time.localtime(e.updated_at))
                console.print(
                    f"  [dim]{when}[/dim] {e.session_id[:8]}  {e.title[:60]}"
                )

        elif cmd == "/new":
            self._persist()
            await self.client.disconnect()
            self.entry = None
            self.session_id = None
            self.resume = None
            self.cost = 0.0
            await self.start()

        else:
            console.print(f"[red]unknown command[/red] {cmd}  [dim]/help[/dim]")

        return False


def run(cfg: Config, resume: str | None = None) -> None:
    asyncio.run(Repl(cfg, resume=resume).run())

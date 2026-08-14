"""Terminal rendering of the SDK message stream."""

from __future__ import annotations

import json
from typing import Any

from rich.console import Console
from rich.markdown import Markdown

console = Console()

# Tool-call one-liners: (tool name) -> the input key worth showing.
_HEADLINE_KEY = {
    "Read": "file_path",
    "Write": "file_path",
    "Edit": "file_path",
    "Glob": "pattern",
    "Grep": "pattern",
    "Bash": "command",
    "WebFetch": "url",
    "WebSearch": "query",
    "Skill": "skill",
    "Task": "description",
}


def _truncate(text: str, limit: int = 110) -> str:
    text = " ".join(str(text).split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def tool_headline(name: str, tool_input: dict[str, Any]) -> str:
    key = _HEADLINE_KEY.get(name)
    if key and key in tool_input:
        return f"{name}({_truncate(tool_input[key])})"
    if not tool_input:
        return name
    return f"{name}({_truncate(json.dumps(tool_input, default=str))})"


class StreamRenderer:
    """Renders assistant text as it streams, tool calls as dim one-liners.

    Text deltas are printed raw while streaming, then the finished block is
    re-rendered as markdown only when it clearly benefits (code fences, lists).
    """

    def __init__(self, show_thinking: bool = False, streaming: bool = True) -> None:
        self.show_thinking = show_thinking
        self.streaming = streaming
        self._streaming_text = False
        self._buffer: list[str] = []

    # -- streaming deltas -------------------------------------------------
    def stream_event(self, event: dict[str, Any]) -> None:
        etype = event.get("type")
        if etype == "content_block_delta":
            delta = event.get("delta", {})
            dtype = delta.get("type")
            if dtype == "text_delta":
                self._begin_text()
                chunk = delta.get("text", "")
                self._buffer.append(chunk)
                console.out(chunk, end="", highlight=False)
            elif dtype == "thinking_delta" and self.show_thinking:
                self._begin_text()
                console.out(delta.get("thinking", ""), end="", style="dim italic")
        elif etype == "content_block_stop":
            self._end_text()

    def _begin_text(self) -> None:
        if not self._streaming_text:
            self._streaming_text = True
            self._buffer = []

    def _end_text(self) -> None:
        if self._streaming_text:
            console.print()
            self._streaming_text = False
            self._buffer = []

    # -- complete messages ------------------------------------------------
    def assistant(self, message: Any) -> None:
        """Render blocks that streaming did not already cover."""
        from claude_agent_sdk.types import TextBlock, ThinkingBlock, ToolUseBlock

        for block in message.content:
            if isinstance(block, ToolUseBlock):
                self._end_text()
                console.print(
                    f"  [cyan]›[/cyan] [dim]{tool_headline(block.name, block.input)}[/dim]"
                )
            elif isinstance(block, TextBlock) and not self.streaming:
                self._end_text()
                console.print(Markdown(block.text))
            elif isinstance(block, ThinkingBlock) and self.show_thinking and not self.streaming:
                console.print(f"[dim italic]{block.thinking}[/dim italic]")
        self._end_text()

    def tool_result(self, message: Any) -> None:
        result = getattr(message, "tool_use_result", None)
        if not isinstance(result, dict):
            return
        if result.get("is_error") or result.get("isError"):
            console.print(f"  [red]✗[/red] [dim]{_truncate(result, 160)}[/dim]")

    def system(self, message: Any) -> None:
        if message.subtype != "init":
            return
        data = message.data or {}
        skills = data.get("skills") or []
        servers = data.get("mcp_servers") or []
        bits = [f"[dim]model[/dim] {data.get('model', '?')}"]
        if skills:
            bits.append(f"[dim]skills[/dim] {len(skills)}")
        if servers:
            ok = sum(1 for s in servers if s.get("status") == "connected")
            bits.append(f"[dim]mcp[/dim] {ok}/{len(servers)}")
        console.print("  ".join(bits))

    def result(self, message: Any) -> None:
        self._end_text()
        if message.is_error:
            errs = ", ".join(message.errors or []) or message.result or ""
            detail = f": {errs}" if errs else ""
            console.print(f"[red]turn failed[/red] ({message.subtype}){detail}")
            return
        parts = [f"{message.num_turns} turns", f"{message.duration_ms / 1000:.1f}s"]
        console.print(f"[dim]{' · '.join(parts)}[/dim]")

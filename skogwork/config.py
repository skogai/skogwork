"""Config resolution.

Layering, lowest to highest precedence:
  1. built-in defaults
  2. ~/.config/skogwork/config.toml
  3. <project>/.skogwork.toml
  4. CLI flags

MCP servers come from the same TOML under [mcp.<name>], and additionally from
a project .mcp.json if present (Claude Code's own format), so existing configs
work unchanged.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # py3.10
    import tomli as tomllib  # type: ignore[no-redef]

USER_CONFIG = Path(
    os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")
) / "skogwork" / "config.toml"

PROJECT_CONFIG = ".skogwork.toml"

# Cowork-ish default toolset: real file access plus a shell.
DEFAULT_TOOLS = [
    "Read",
    "Write",
    "Edit",
    "Glob",
    "Grep",
    "Bash",
    "WebFetch",
    "WebSearch",
    "TodoWrite",
    "Task",
    "Skill",
]


@dataclass
class Config:
    cwd: Path
    model: str | None = None
    permission_mode: str = "acceptEdits"
    allowed_tools: list[str] = field(default_factory=lambda: list(DEFAULT_TOOLS))
    disallowed_tools: list[str] = field(default_factory=list)
    setting_sources: list[str] = field(default_factory=lambda: ["user", "project"])
    skills: list[str] | str = "all"
    mcp_servers: dict[str, Any] = field(default_factory=dict)
    system_prompt: Any = None
    add_dirs: list[str] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)
    max_budget_usd: float | None = None

    def to_options_kwargs(self) -> dict[str, Any]:
        kw: dict[str, Any] = {
            "cwd": str(self.cwd),
            "permission_mode": self.permission_mode,
            "allowed_tools": self.allowed_tools,
            "disallowed_tools": self.disallowed_tools,
            "setting_sources": self.setting_sources,
            "skills": self.skills,
            "mcp_servers": self.mcp_servers,
            "add_dirs": self.add_dirs,
            "env": self.env,
            "include_partial_messages": True,
        }
        if self.model:
            kw["model"] = self.model
        if self.system_prompt is not None:
            kw["system_prompt"] = self.system_prompt
        if self.max_budget_usd is not None:
            kw["max_budget_usd"] = self.max_budget_usd
        return kw


def _read_toml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    with path.open("rb") as fh:
        return tomllib.load(fh)


def _read_mcp_json(project: Path) -> dict[str, Any]:
    path = project / ".mcp.json"
    if not path.is_file():
        return {}
    data = json.loads(path.read_text())
    return data.get("mcpServers", data)


def _merge(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    out = dict(base)
    for key, value in overlay.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _merge(out[key], value)
        else:
            out[key] = value
    return out


def _expand_env(servers: dict[str, Any]) -> dict[str, Any]:
    """Expand ${VAR} in env values and headers so secrets stay out of the file."""
    def expand(value: Any) -> Any:
        if isinstance(value, str):
            return os.path.expandvars(value)
        if isinstance(value, dict):
            return {k: expand(v) for k, v in value.items()}
        if isinstance(value, list):
            return [expand(v) for v in value]
        return value

    return {name: expand(cfg) for name, cfg in servers.items()}


def load(cwd: Path, overrides: dict[str, Any] | None = None) -> Config:
    raw = _merge(_read_toml(USER_CONFIG), _read_toml(cwd / PROJECT_CONFIG))

    mcp = _read_mcp_json(cwd)
    mcp = _merge(mcp, raw.pop("mcp", {}) or {})

    agent = raw.get("agent", {})
    cfg = Config(cwd=cwd)

    if "model" in agent:
        cfg.model = agent["model"]
    if "permission_mode" in agent:
        cfg.permission_mode = agent["permission_mode"]
    if "tools" in agent:
        cfg.allowed_tools = list(agent["tools"])
    if "disallowed_tools" in agent:
        cfg.disallowed_tools = list(agent["disallowed_tools"])
    if "setting_sources" in agent:
        cfg.setting_sources = list(agent["setting_sources"])
    if "skills" in agent:
        cfg.skills = agent["skills"]
    if "add_dirs" in agent:
        cfg.add_dirs = [str(Path(p).expanduser()) for p in agent["add_dirs"]]
    if "system_prompt" in agent:
        cfg.system_prompt = agent["system_prompt"]
    if "max_budget_usd" in agent:
        cfg.max_budget_usd = float(agent["max_budget_usd"])

    cfg.env = dict(raw.get("env", {}))
    cfg.mcp_servers = _expand_env(mcp)

    for key, value in (overrides or {}).items():
        if value is not None:
            setattr(cfg, key, value)

    # Skill tool must be present when an explicit tool list is given.
    if cfg.skills and "Skill" not in cfg.allowed_tools:
        cfg.allowed_tools.append("Skill")

    return cfg

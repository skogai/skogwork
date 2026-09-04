## Where the real leverage is

skogwork sits directly on `ClaudeAgentOptions` (not on `settings.json`), so the SDK's own dataclass fields are the primary knob — env vars are secondary/fallback. Here's what actually controls "how much stuff loads at session start."

### Field semantics (verified against the resolved config, not just the docs)

skogwork's `CLAUDE.md` says _"tool access is controlled solely by `[agent] tools` in config."_ That prose reads as if `[agent] tools` were the only knob, but `config.py` actually keeps three distinct fields, and `tools` — the restricting one — is already wired through to `ClaudeAgentOptions`:

| Field                                                                     | Effect                                                                                                                                                                                      |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `allowed_tools`                                                           | Auto-_approves_ the listed tools (skips the permission prompt). Anything not covered by `tools`/`disallowed_tools` is **still loaded into context** and still callable — it just falls through to `permission_mode`. |
| `disallowed_tools`                                                        | A bare name (`"Bash"`) actually **removes that tool's definition** from the request. `"*"` removes everything.                                                                              |
| `tools` (`list[str] \| {"type":"preset","preset":"claude_code"} \| None`) | The actual tool-set selector — the SDK/CLI equivalent of `--tools "Bash,Edit,Read"`. This is what restricts what Claude _sees_, not just what it can do without asking.                     |

Confirmed live via `skogwork --config`: `config.py` already has a `tools: list[str] | None` field (`config.py:54`), separate from `allowed_tools`/`disallowed_tools`, force-appends `"Skill"` when skills are enabled (`config.py:164-165`, mirroring the `allowed_tools` append CLAUDE.md already documents), and passes straight through to `ClaudeAgentOptions(tools=...)`. `~/.config/skogwork/config.toml` sets it explicitly to an 11-item list, so this repo's sessions are *not* carrying full definitions for the ~40-strong built-in surface (`Agent`, `Artifact`, `AskUserQuestion`, `CronCreate/Delete/List`, `EndConversation`, `EnterPlanMode`, `EnterWorktree`, `ExitPlanMode`, `ExitWorktree`, `ListAgents`, `ListMcpResourcesTool`, `LSP`, `Monitor`, `NotebookEdit`, `PowerShell`, `PushNotification`, `ReadMcpResourceTool`, `RemoteTrigger`, `ReportFindings`, `ScheduleWakeup`, `SendMessage`, `SendUserFile`, `ShareOnboardingGuide`, `TaskCreate/Get/List/Update`, `ToolSearch`, `WaitForMcpServers`, `Workflow`, etc.) — that surface is already stripped, and `allowed_tools`/`disallowed_tools` are layered on top for auto-approval and hard vetoes (including scoped ones like `Bash(rm *)`, which work even under `bypassPermissions`).

`CLAUDE.md`'s wording has been updated to spell out the three-field split instead of implying `[agent] tools` alone controls access.

### The four biggest context-cost levers (from `features-overview.md`)

| Feature           | Loads                                            | Cost                                                                                                                                                                            | Off switch                                                                    |
| ----------------- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| **System prompt** | Always                                           | `claude_code` preset is large (tool guidance, style rules, env context); the SDK's default when `system_prompt` is unset is a **minimal prompt** with just tool-calling support | Leave `system_prompt=None` for minimal; only opt into the preset deliberately |
| **CLAUDE.md**     | Session start, full content, every request       | Can be large; no on-demand loading                                                                                                                                              | `setting_sources=[]`, or per-source omission, or `claudeMdExcludes`           |
| **Skills**        | Descriptions at start (low), full content on use | Near-zero if `disable-model-invocation: true` or `skills=[]`                                                                                                                    | `skills=[]`                                                                   |
| **MCP servers**   | Tool names at start, schemas deferred            | Low with tool search on; can spike if `ENABLE_TOOL_SEARCH=false` or many `alwaysLoad` tools                                                                                     | `mcp_servers={}` + `strict_mcp_config=True`                                   |

Subagents and hooks are effectively free at session start (isolated context / external execution).

### `ClaudeAgentOptions` fields to actually build the strip-down around

| Field              | Set to (bare)                                                                     | Then build up with                                                                                                              |
| ------------------ | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `tools`            | `[]` or a short explicit list                                                     | Add tool names back one at a time                                                                                               |
| `setting_sources`  | `[]`                                                                              | Add `"project"`, `"user"`, `"local"` individually — each pulls in CLAUDE.md, rules, skills, hooks, settings.json for that scope |
| `system_prompt`    | leave unset (`None`)                                                              | Only set `{"type":"preset","preset":"claude_code"}` (+`append`) when you want the full CLI-equivalent behavior                  |
| `mcp_servers`      | `{}`                                                                              | Add servers explicitly; use `strict_mcp_config=True` to also block `.mcp.json`/claude.ai connectors from sneaking in            |
| `skills`           | `[]`                                                                              | `"all"` or an explicit name list once you want skill descriptions back                                                          |
| `agents`           | omit                                                                              | Define your own subagents explicitly instead of inheriting built-ins                                                            |
| `disallowed_tools` | `["*"]` if using `tools` isn't granular enough, or scoped rules like `Bash(rm *)` | Loosen per-tool                                                                                                                 |

Note: `settingSources: []` still doesn't stop everything — `~/.claude.json`, managed/policy settings, and (unless you also set `strict_mcp_config: true` or `disableClaudeAiConnectors`) claude.ai MCP connectors load regardless. For real isolation the docs explicitly recommend `setting_sources=[]` **plus** `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` in `env`.

### Env vars worth wiring into skogwork's `env` map

Grouped by what they strip:

**Tools / agents**

- `CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS=1` — drops built-in subagent types (Explore, Plan). Non-interactive only.
- `ENABLE_TOOL_SEARCH` — `auto`/`auto:N`/`false`/`true`; controls whether tool _schemas_ (not names) load upfront. Matters once MCP servers are added back.

**Memory / project context**

- `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` — stops the `~/.claude/projects/<project>/memory/` auto-memory read/write (this is the one input that's read even with `setting_sources=[]`).

**Skills / commands**

- `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS=1` — removes bundled skills/workflows entirely (not just hides them).
- `DISABLE_DOCTOR_COMMAND=1` — hides `/doctor` from the model too.

**MCP**

- `ENABLE_CLAUDEAI_MCP_SERVERS=false` — blocks claude.ai connector auto-load (survives `setting_sources=[]`).

**Misc bloat/noise, not token-costly but worth knowing for a "nothing extra" baseline**

- `CLAUDE_CODE_DISABLE_ARTIFACT=1`, `CLAUDE_CODE_DISABLE_AGENT_VIEW=1` (kills `Artifact`, background-agent surface)
- `DISABLE_AUTOUPDATER=1`, `DISABLE_TELEMETRY`, `DISABLE_ERROR_REPORTING`, `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`
- `CLAUDE_CODE_ENABLE_TASKS=0`/unset — keeps `TaskCreate/Get/List/Update` off in favor of nothing, since `TodoWrite` is already in skogwork's default list and the two are mutually exclusive-ish

**Thinking budget**

- `thinking` / `effort` fields (or `MAX_THINKING_TOKENS=0` via env) if extended thinking tokens matter for your budget.

### Reference point: what Anthropic itself calls "stripped"

Two CLI flags are useful mental models even though skogwork uses the SDK directly, not `claude -p`:

- **`--bare`**: skips hooks, skills, plugins, MCP, auto memory, CLAUDE.md; leaves only Bash + Read + Edit; explicitly _"the recommended mode for scripted and SDK calls."_ This is roughly `tools=["Bash","Read","Edit"]` + `setting_sources=[]` + `mcp_servers={}`.
- **`--safe-mode`**: opposite intent — keeps everything functional but disables all _customization_ sources (CLAUDE.md, skills, plugins, hooks, MCP, output styles, workflows, LSP, auto memory) for debugging a broken config, while built-in tools/permissions stay normal. Useful if you ever need "is my stripped-down config the problem" diagnostics.

**Bottom line for skogwork's `config.py`:** the `tools` (restrict) field distinct from `allowed_tools` (auto-approve) already exists and is populated in `~/.config/skogwork/config.toml` — verified via `skogwork --config`. Nothing left to build there; the only fix needed was to `CLAUDE.md`'s wording, now done.

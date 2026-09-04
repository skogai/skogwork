# Claude Code Documentation Overview

## Use Claude Code with a screen reader
_source: https://code.claude.com/docs/en/accessibility_

- Turn on screen reader mode
- Turn off screen reader mode
- Accessibility settings
- What your screen reader hears
- Answer menus and prompts
- Hear when Claude Code needs you
- Known limitations
- Report an issue

## Set up Claude Code for your organization
_source: https://code.claude.com/docs/en/admin-setup_

- Choose your API provider
- Decide how settings reach devices
- Decide what to enforce
- Set up usage visibility
- Review data handling
- Verify and onboard
- Next steps

## Escalate hard decisions with the advisor tool
_source: https://code.claude.com/docs/en/advisor_

- When to use the advisor
- Enable the advisor
- Choose an advisor model
- When Claude consults the advisor
- What you see during a session
- Cost
- Impact on prompt caching
- Requirements
- Turn the advisor off
- Compare with related features
- See also

```
/advisor opus
```

## Run agents in parallel
_source: https://code.claude.com/docs/en/agents_

- Choose an approach
- Check on running work
- Learn more

## How the agent loop works
_source: https://code.claude.com/docs/en/agent-sdk/agent-loop_

- The loop at a glance
- Turns and messages
- Message types
- Tool execution
- Control how the loop runs
- The context window
- Sessions and continuity
- Handle the result
- Hooks
- Put it all together
- Next steps

## Use Claude Code features in the SDK
_source: https://code.claude.com/docs/en/agent-sdk/claude-code-features_

- Control filesystem settings with settingSources
- Project instructions (CLAUDE.md and rules)
- Skills
- Hooks
- Choose the right feature
- Related resources

## Track cost and usage
_source: https://code.claude.com/docs/en/agent-sdk/cost-tracking_

- Understand token usage
- Track costs in streaming input mode
- Get the total cost of a query
- Track per-step and per-model usage
- Accumulate costs across multiple calls
- Handle errors, caching, and output token counts
- Related documentation

```
import { query } from "@anthropic-ai/claude-agent-sdk";
```

## Give Claude custom tools
_source: https://code.claude.com/docs/en/agent-sdk/custom-tools_

- Quick reference
- Create a custom tool
- Control tool access
- Handle errors
- Return images and resources
- Return structured data
- Example: unit converter
- Next steps

```
return {
```

## Examples
_source: https://code.claude.com/docs/en/agent-sdk/examples_

- Run a minimal agent first
- Explore a TypeScript application
- Work through a Python recipe

## Rewind file changes with checkpointing
_source: https://code.claude.com/docs/en/agent-sdk/file-checkpointing_

- How checkpointing works
- Implement checkpointing
- Common patterns
- Try it out
- Limitations
- Troubleshooting
- Next steps

```
CLAUDE_CODE_ENABLE_SDK_FILE_CHECKPOINTING=true claude -p --resume <session-id> --rewind-files <checkpoint-uuid>
```

## Intercept and control agent behavior with hooks
_source: https://code.claude.com/docs/en/agent-sdk/hooks_

- How hooks work
- Available hooks
- Configure hooks
- Examples
- Fix common issues
- Related resources

```
const myHook: HookCallback = async (input, toolUseID, { signal }) => {
```

## Hosting the Agent SDK
_source: https://code.claude.com/docs/en/agent-sdk/hosting_

- The subprocess model
- Choose a session pattern
- Provision the container
- Handle production concerns
- Known limitations
- Troubleshoot deployment failures
- Next steps

```
CLAUDE_CODE_ENABLE_TELEMETRY=1
```

## Connect to external tools with MCP
_source: https://code.claude.com/docs/en/agent-sdk/mcp_

- Quickstart
- Add an MCP server
- Connection timing
- Allow MCP tools
- Transport types
- MCP tool search
- Authentication
- Examples
- Error handling
- Troubleshooting
- Related resources

```
{
```

## Migrate to Claude Agent SDK
_source: https://code.claude.com/docs/en/agent-sdk/migration-guide_

- Overview
- What's Changed
- Migration Steps
- Breaking changes
- Next Steps

```
npm uninstall @anthropic-ai/claude-code
```

## Modifying system prompts
_source: https://code.claude.com/docs/en/agent-sdk/modifying-system-prompts_

- How system prompts work
- Customize agent behavior
- Compare the four approaches
- Combine approaches
- See also

```
---
```

## Observability with OpenTelemetry
_source: https://code.claude.com/docs/en/agent-sdk/observability_

- How telemetry flows from the SDK
- Enable telemetry export
- Read agent traces
- Link traces to your application
- Tag telemetry from your agent
- Attribute actions to your end users
- Control sensitive data in exports
- Related documentation

## Agent SDK overview
_source: https://code.claude.com/docs/en/agent-sdk/overview_

- Compare the Agent SDK to other Claude tools
- Capabilities
- Get started
- Changelog
- Report bugs
- Branding guidelines
- License and terms
- Next steps

## Configure permissions
_source: https://code.claude.com/docs/en/agent-sdk/permissions_

- How permissions are evaluated
- Allow and deny rules
- Permission modes
- Related resources

```
const options = {
```

## Plugins in the SDK
_source: https://code.claude.com/docs/en/agent-sdk/plugins_

- Loading plugins
- Verifying plugin installation
- Using plugin skills
- Complete example
- Plugin structure reference
- Multiple plugin sources
- Troubleshooting
- See also

```
my-plugin/
```

## Agent SDK reference - Python
_source: https://code.claude.com/docs/en/agent-sdk/python_

- Installation
- Choosing between `query()` and `ClaudeSDKClient`
- Functions
- Classes
- Types
- Message Types
- Content Block Types
- Error Types
- Hook Types
- Tool Input/Output Types
- Build a continuous conversation interface
- Error handling
- Sandbox Configuration
- See also

```
python3 -m venv .venv
```

## Quickstart
_source: https://code.claude.com/docs/en/agent-sdk/quickstart_

- Prerequisites
- Setup
- Create a buggy file
- Build an agent that finds and fixes bugs
- Key concepts
- Next steps

```
def calculate_average(numbers):
```

## Securely deploying AI agents
_source: https://code.claude.com/docs/en/agent-sdk/secure-deployment_

- Threat model
- Built-in security features
- Security principles
- Isolation technologies
- Credential management
- Filesystem configuration
- Further reading

```
npm install @anthropic-ai/sandbox-runtime
```

## Work with sessions
_source: https://code.claude.com/docs/en/agent-sdk/sessions_

- Choose an approach
- Automatic session management
- Use session options with `query()`
- Resume across hosts
- Related resources

```
import asyncio
```

## Persist sessions to external storage
_source: https://code.claude.com/docs/en/agent-sdk/session-storage_

- The `SessionStore` interface
- Quick start
- Write your own adapter
- Reference implementations
- Behavior notes
- Supported on
- Related resources

```
import { query } from "@anthropic-ai/claude-agent-sdk";
```

## Extend agents with skills
_source: https://code.claude.com/docs/en/agent-sdk/skills_

- How skills work with the Agent SDK
- Use skills with the Agent SDK
- Commands in Agent SDK sessions
- Create skills
- Pre-approve tools for skills
- Troubleshooting
- Next steps
- Related resources

```
Available commands: ["clear", "compact", "context", "usage", "code-review", "verify", "security-check", ...]
```

## Stream responses in real-time
_source: https://code.claude.com/docs/en/agent-sdk/streaming-output_

- Enable streaming output
- StreamEvent reference
- Message flow
- Stream tool calls
- Build a streaming UI
- Known limitations
- Next steps

```
StreamEvent (message_start)
```

## Streaming Input
_source: https://code.claude.com/docs/en/agent-sdk/streaming-vs-single-mode_

- Overview
- Streaming Input Mode (Recommended)
- Single Message Input

## Get structured output from agents
_source: https://code.claude.com/docs/en/agent-sdk/structured-outputs_

- Why structured outputs?
- Quick start
- Type-safe schemas with Zod and Pydantic
- Output format configuration
- Example: TODO tracking agent
- Error handling
- Related resources

## Subagents in the SDK
_source: https://code.claude.com/docs/en/agent-sdk/subagents_

- Overview
- Benefits of using subagents
- Create subagents
- What subagents inherit
- Invoke subagents
- Detect subagent invocation
- Resume subagents
- Tool restrictions
- Cap subagent depth, concurrency, and spend
- Scale up with dynamic workflows
- Troubleshooting
- Related documentation

```
"Use the code-reviewer agent to check the authentication module"
```

## Track todos
_source: https://code.claude.com/docs/en/agent-sdk/todo-tracking_

- Model availability
- Todo lifecycle
- When Claude creates todos
- Examples
- Related documentation

## Scale to many tools with tool search
_source: https://code.claude.com/docs/en/agent-sdk/tool-search_

- How tool search works
- Configure tool search
- Optimize tool discovery
- Limits
- Related documentation

## Troubleshooting
_source: https://code.claude.com/docs/en/agent-sdk/troubleshooting_

- CLI startup
- CLI process exit
- Structured outputs
- Report a new issue

```
Claude Code not found at: /your/configured/path
```

## Agent SDK reference - TypeScript
_source: https://code.claude.com/docs/en/agent-sdk/typescript_

- Installation
- Functions
- Types
- Message Types
- Hook Types
- Tool Input Types
- Tool Output Types
- Permission Types
- Other Types
- Sandbox Configuration
- See also

```
npm install @anthropic-ai/claude-agent-sdk
```

## TypeScript SDK V2 session API (removed)
_source: https://code.claude.com/docs/en/agent-sdk/typescript-v2-preview_

- Installation
- Quick start
- API reference
- Feature availability
- See also

```
npm install @anthropic-ai/claude-agent-sdk@0.2
```

## Handle approvals and user input
_source: https://code.claude.com/docs/en/agent-sdk/user-input_

- Detect when Claude needs input
- Handle tool approval requests
- Handle clarifying questions
- Limitations
- Other ways to get user input
- Related resources

```
{
```

## Orchestrate teams of Claude Code sessions
_source: https://code.claude.com/docs/en/agent-teams_

- When to use agent teams
- Enable agent teams
- Start your first agent team
- Control your agent team
- How agent teams work
- Use case examples
- Best practices
- Troubleshooting
- Limitations
- Next steps

```
{
```

## Manage multiple agents with agent view
_source: https://code.claude.com/docs/en/agent-view_

- Quick start
- Monitor sessions with agent view
- Dispatch new agents
- Manage sessions from the shell
- How background sessions are hosted
- Troubleshooting
- Limitations
- Related resources
- Version history

```
claude agents --cwd ~/projects/my-app
```

## Claude Code on Amazon Bedrock
_source: https://code.claude.com/docs/en/amazon-bedrock_

- Prerequisites
- Sign in with Bedrock
- Set up manually
- Startup model checks
- Cross-region inference profile prefixes
- IAM configuration
- 1M token context window
- Service tiers
- AWS Guardrails
- Use the Mantle endpoint
- Troubleshooting
- Additional resources

```
aws configure
```

## Track team usage with analytics
_source: https://code.claude.com/docs/en/analytics_

- Access analytics for Team and Enterprise
- Access analytics for API customers
- Related resources

## Share session output as artifacts
_source: https://code.claude.com/docs/en/artifacts_

- When to use an artifact
- Create an artifact
- Update an artifact
- Find an artifact again
- Share an artifact
- Collect comments on an artifact
- Pull live data with MCP connectors
- What you can build
- Improve the visual design
- Design system
- Draft a design canvas
- Page constraints
- Availability
- Disable artifacts
- Manage artifacts for your organization
- Related resources

```
Make an artifact that walks through this PR with the diff annotated inline.
```

## Authentication
_source: https://code.claude.com/docs/en/authentication_

- Log in to Claude Code
- Set up team authentication
- Credential management

```
claude setup-token
```

## Configure auto mode
_source: https://code.claude.com/docs/en/auto-mode-config_

- Common boundaries
- Where the classifier reads configuration
- Define trusted infrastructure
- Override the block and allow rules
- Route all shell commands through the classifier
- Inspect the defaults and your effective config
- Review denials
- See also

```
{
```

## Best practices for Claude Code
_source: https://code.claude.com/docs/en/best-practices_

- Give Claude a way to verify its work
- Explore first, then plan, then code
- Provide specific context in your prompts
- Configure your environment
- Communicate effectively
- Manage your session
- Automate and scale
- Avoid common failure patterns
- Develop your intuition
- Related resources

```
# Code style
```

## Champion kit
_source: https://code.claude.com/docs/en/champion-kit_

- The champion role
- Share what you discover
- Be the person people ask
- Grow the circle
- Respond to common concerns
- Quick-reference sheet

```
Learned today that @-mentioning a directory works. I pointed it at
```

## Claude Code changelog
_source: https://code.claude.com/docs/en/changelog_

## Push events into a running session with channels
_source: https://code.claude.com/docs/en/channels_

- Supported channels
- Quickstart
- Security
- Enterprise controls
- Research preview
- How channels compare
- Next steps

```
{
```

## Channels reference
_source: https://code.claude.com/docs/en/channels-reference_

- Overview
- What you need
- Example: build a webhook receiver
- Test during the research preview
- Server options
- Notification format
- Expose a reply tool
- Gate inbound messages
- Relay permission prompts
- Package as a plugin
- See also

```
# Testing a plugin you're developing
```

## Checkpointing
_source: https://code.claude.com/docs/en/checkpointing_

- How checkpoints work
- Common use cases
- Limitations
- See also

```
rm file.txt
```

## Use Claude Code with Chrome
_source: https://code.claude.com/docs/en/chrome_

- Capabilities
- Prerequisites
- Get started in the CLI
- Example workflows
- Troubleshooting
- See also

```
I just updated the login form validation. Can you open localhost:3000,
```

## Claude apps gateway for Amazon Bedrock, Claude Platform on AWS, Google Cloud, and Microsoft Foundry
_source: https://code.claude.com/docs/en/claude-apps-gateway_

- Why Claude apps gateway
- Quickstart
- Connect developers
- Availability and limitations
- Next steps

```
openssl x509 -noout -fingerprint -sha256 -in cert.pem | cut -d= -f2 | tr -d : | tr 'A-F' 'a-f'
```

## Claude apps gateway configuration
_source: https://code.claude.com/docs/en/claude-apps-gateway-config_

- File structure
- Secret expansion
- Required sections
- Optional sections
- Complete example
- Client-side managed settings
- Related

```
upstreams:
```

## Claude apps gateway deployment and operations
_source: https://code.claude.com/docs/en/claude-apps-gateway-deploy_

- Identity provider setup
- Deployment
- Operations
- Security
- Troubleshooting
- Related

## Deploy Claude apps gateway on AWS
_source: https://code.claude.com/docs/en/claude-apps-gateway-on-aws_

- Architecture
- Prerequisites
- Deploy the gateway
- Terraform reference
- Troubleshooting
- Telemetry
- Next steps

```
aws ec2 describe-subnets --filters "Name=vpc-id,Values=<your-vpc-id>" \
```

## Deploy Claude apps gateway on Google Cloud
_source: https://code.claude.com/docs/en/claude-apps-gateway-on-gcp_

- What you'll build
- Prerequisites
- Deploy the gateway
- Terraform reference
- Troubleshooting
- Next steps

```
export PROJECT_ID=<your-project>
```

## Claude apps gateway spend limits
_source: https://code.claude.com/docs/en/claude-apps-gateway-spend-limits_

- Set a cap
- How enforcement works
- Admin API reference
- Data lifecycle
- Related

```
curl -sS https://claude-gateway.internal.example.com/v1/organizations/spend_limits \
```

## Use Claude Code on the web
_source: https://code.claude.com/docs/en/claude-code-on-the-web_

- Cloud environments
- GitHub authentication options
- Move tasks between web and terminal
- Work with sessions
- Auto-fix pull requests
- Security and isolation
- Troubleshooting
- Limitations
- Related resources

```
claude --cloud "Fix the authentication bug in src/auth/login.ts"
```

## Explore the .claude directory
_source: https://code.claude.com/docs/en/claude-directory_

- Commands
- Stack
- Rules
- Diff to review
- Input Validation
- Authentication
- Patterns seen
- Recurring issues
- Project
- Reference
- Auth Token Issues
- Database Connection Drops
- Explore the directory
- What's not shown
- Choose the right file
- File reference
- Troubleshoot configuration
- Application data
- Related resources

```
claude project purge ~/work/my-repo --dry-run
```

## Claude Code on Claude Platform on AWS
_source: https://code.claude.com/docs/en/claude-platform-on-aws_

- Prerequisites
- Setup
- Use the Agent SDK
- Route through a corporate proxy
- Troubleshooting
- Additional resources

```
aws sso login --profile my-profile
```

## Scan your codebase for vulnerabilities
_source: https://code.claude.com/docs/en/claude-security_

- Prerequisites
- Install the plugin
- Scan and fix your codebase
- Fix findings
- How the plugin fits with other security tools
- Troubleshooting
- Related resources

```
/plugin install claude-security@claude-plugins-official
```

## Claude Tag
_source: https://code.claude.com/docs/en/claude-tag_

## CLI reference
_source: https://code.claude.com/docs/en/cli-reference_

- CLI commands
- CLI flags
- See also

## Configure cloud environments
_source: https://code.claude.com/docs/en/cloud-environments_

- The Default environment
- Configure your environment
- Network access
- What's available in cloud sessions
- Setup scripts
- Default allowed domains
- Related resources

```
NODE_ENV=development
```

## Code Review
_source: https://code.claude.com/docs/en/code-review_

- How reviews work
- Set up Code Review
- Manually trigger reviews
- Customize reviews
- What Important means here
- Cap the nits
- Do not report
- Always check
- View usage
- Pricing
- Troubleshooting
- Review a diff locally
- Related resources

```
gh api repos/OWNER/REPO/check-runs/CHECK_RUN_ID \
```

## Commands
_source: https://code.claude.com/docs/en/commands_

- Commands across a typical workflow
- All commands
- How the command menu matches what you type
- MCP prompts
- See also

## Common workflows
_source: https://code.claude.com/docs/en/common-workflows_

- Prompt recipes
- Resume previous conversations
- Run parallel sessions with worktrees
- Plan before editing
- Delegate research to subagents
- Pipe Claude into scripts
- Next steps

```
can Claude Code create pull requests?
```

## Communications kit
_source: https://code.claude.com/docs/en/communications-kit_

- Launch communications
- Tips and tricks campaign
- Quick reference

```
Subject: You're in the Claude Code pilot
```

## Let Claude use your computer from the CLI
_source: https://code.claude.com/docs/en/computer-use_

- What you can do with computer use
- When computer use applies
- Enable computer use
- Approve apps per session
- How Claude works on your screen
- Safety and the trust boundary
- Example workflows
- Differences from the Desktop app
- Troubleshooting
- See also

```
Build the app target, launch it, and click through each tab to make
```

## Explore the context window
_source: https://code.claude.com/docs/en/context-window_

- What the timeline shows
- What survives compaction
- When your context fills up
- Check your own session
- Related resources

## Run Claude Code behind a corporate launcher
_source: https://code.claude.com/docs/en/corporate-launcher_

- What the launcher covers
- Set up the launcher
- The launcher contract
- Relationship to `CLAUDE_CODE_SHELL_PREFIX`
- Related resources

## Manage costs effectively
_source: https://code.claude.com/docs/en/costs_

- Track your costs
- Manage costs for your organization
- Reduce token usage
- Background token usage
- Why usage climbs in a long session
- Understanding changes in Claude Code behavior

```
Total cost:            $0.55
```

## Message your other Claude Code sessions
_source: https://code.claude.com/docs/en/cross-session-messaging_

- When to use cross-session messaging
- Message another session
- How a session treats an incoming message
- Restrict cross-session messaging
- Availability
- Limitations
- Related resources

```
Ask the session running in my other terminal whether the migration finished
```

## Data usage
_source: https://code.claude.com/docs/en/data-usage_

- Data policies
- Data access
- Local Claude Code: Data flow and dependencies
- Telemetry services
- Default behaviors by API provider

## Debug your configuration
_source: https://code.claude.com/docs/en/debug-your-config_

- See what loaded into context
- Check resolved settings
- Check MCP servers
- Check hooks
- Test against a clean configuration
- Check common causes
- Related resources

```
cd /tmp && CLAUDE_CONFIG_DIR=/tmp/claude-clean claude
```

## Launch sessions from links
_source: https://code.claude.com/docs/en/deep-links_

- How deep links work
- Build a link
- Examples
- High 5xx rate on web-gateway
- Registration and supported platforms
- Open a VS Code tab instead of a terminal
- Troubleshooting
- Learn more

```
claude-cli://open
```

## Desktop application
_source: https://code.claude.com/docs/en/desktop_

- Start a session
- Work with code
- Arrange your workspace
- Let Claude use your computer
- Manage sessions
- Extend Claude Code
- Environment configuration
- Enterprise configuration
- Coming from the CLI?
- Troubleshooting

```
{
```

## Test iOS apps in the simulator
_source: https://code.claude.com/docs/en/desktop-ios-simulator_

- Requirements
- Run your app in the simulator
- Control the simulator yourself
- How sessions manage devices
- Grant Claude access to a device
- Limitations
- Troubleshooting
- See also

```
sudo xcode-select -s /Applications/Xcode-26.4.app
```

## Claude Desktop on Linux (beta)
_source: https://code.claude.com/docs/en/desktop-linux_

- Requirements
- Install
- Update
- Uninstall
- Troubleshoot
- What's not in the Linux beta yet

```
curl -fLO "https://downloads.claude.ai/claude-desktop/apt/stable/$(curl -s "https://downloads.claude.ai/claude-desktop/apt/stable/dists/stable/main/binary-$(dpkg --print-architecture)/Packages" | grep '^Filename: pool/main/c/claude-desktop/claude-desktop_' | sort -V | tail -n 1 | cut -d' ' -f2)"
```

## Get started with the desktop app
_source: https://code.claude.com/docs/en/desktop-quickstart_

- Install
- Start your first session
- Now what?
- Coming from the CLI?
- What's next

## Schedule recurring tasks in Claude Code Desktop
_source: https://code.claude.com/docs/en/desktop-scheduled-tasks_

- Compare scheduling options
- Create a scheduled task
- Schedule options
- How scheduled tasks run
- Missed runs
- Permissions for scheduled tasks
- Manage scheduled tasks
- Related resources

## Claude Code Desktop in WSL
_source: https://code.claude.com/docs/en/desktop-wsl_

- Requirements
- Start a WSL session
- What works in a WSL session
- Managed devices

## Development containers
_source: https://code.claude.com/docs/en/devcontainer_

- Add Claude Code to your dev container
- Persist authentication and settings across rebuilds
- Enforce organization policy
- Restrict network egress
- Run without permission prompts
- Try the reference container
- Next steps

```
"mounts": [
```

## Discover and install prebuilt plugins through marketplaces
_source: https://code.claude.com/docs/en/discover-plugins_

- How marketplaces work
- Official Anthropic marketplace
- Community marketplace
- Try it: add the demo marketplace
- Add marketplaces
- Install plugins
- Manage installed plugins
- Manage marketplaces
- Configure team marketplaces
- Security
- Troubleshooting
- Next steps

```
/plugin install github@claude-plugins-official
```

## Environment variables
_source: https://code.claude.com/docs/en/env-vars_

- Set environment variables
- Precedence
- Variables
- Features that need feature-flag fetching
- See also

```
{
```

## Error reference
_source: https://code.claude.com/docs/en/errors_

- Find your error
- Automatic retries
- Server errors
- Usage limits
- Authentication errors
- Network and connection errors
- Request errors
- Installation errors
- Command-line errors
- Plugin errors
- Tool errors
- Background session errors
- Wrapper and IDE errors
- Rewind warnings
- Session saving warnings
- Configuration warnings
- Responses seem lower quality than usual
- Report an error

```
API Error: 500 Internal server error. This is a server-side issue, usually temporary — try again in a moment. If it persists, check https://status.claude.com.
```

## Speed up responses with fast mode
_source: https://code.claude.com/docs/en/fast-mode_

- Toggle fast mode
- Understand the cost tradeoff
- Decide when to use fast mode
- Requirements
- Handle rate limits
- Research preview
- See also

```
{
```

## Feature availability
_source: https://code.claude.com/docs/en/feature-availability_

- Availability by model provider
- Availability by subscription plan
- Model availability
- Related resources

## Extend Claude Code
_source: https://code.claude.com/docs/en/features-overview_

- Overview
- Match features to your goal
- Understand context costs
- Learn more

## Fullscreen rendering
_source: https://code.claude.com/docs/en/fullscreen_

- Enable fullscreen rendering
- What changes
- Use the mouse
- Scroll the conversation
- Search and review the conversation
- Clear the conversation
- Use with tmux
- Keep native text selection
- Troubleshooting
- Research preview

```
CLAUDE_CODE_NO_FLICKER=1 claude
```

## Run Claude Code through a gateway
_source: https://code.claude.com/docs/en/gateways_

- How a gateway works
- Choose a gateway
- Subscriptions and gateways
- Configure separately from the gateway
- Next steps

## Claude Code GitHub Actions
_source: https://code.claude.com/docs/en/github-actions_

- Setup
- Interactive and automation modes
- Example use cases
- Best practices
- Use a cloud provider
- Troubleshooting
- Advanced configuration
- Upgrade from beta
- What's next

```
name: Claude Code
```

## Use Claude Code GitHub Actions with cloud providers
_source: https://code.claude.com/docs/en/github-actions-cloud-providers_

- Choose your provider
- Prerequisites
- Set up the integration
- Troubleshooting
- What's next

```
- uses: anthropics/claude-code-action@v1
```

## Claude Code with GitHub Enterprise Server
_source: https://code.claude.com/docs/en/github-enterprise-server_

- What works with GitHub Enterprise Server
- Admin setup
- Developer workflow
- Plugin marketplaces on GHES
- Limitations
- Troubleshooting
- Related resources

```
git clone git@github.example.com:platform/api-service.git
```

## Claude Code GitLab CI/CD
_source: https://code.claude.com/docs/en/gitlab-ci-cd_

- Why use Claude Code with GitLab?
- How it works
- What can Claude do?
- Setup
- Example use cases
- Using with Amazon Bedrock and Google Cloud
- Configuration examples
- Best practices
- Troubleshooting
- Advanced configuration

```
stages:
```

## Glossary
_source: https://code.claude.com/docs/en/glossary_

- A
- B
- C
- D
- E
- H
- M
- N
- O
- P
- R
- S
- T
- V
- W
- Deprecated and renamed terms

## Keep Claude working toward a goal
_source: https://code.claude.com/docs/en/goal_

- Compare ways to keep a session running
- Use `/goal`
- How evaluation works
- Requirements
- See also

```
/goal all tests in test/auth pass and the lint step is clean
```

## Claude Code on Google Cloud's Agent Platform
_source: https://code.claude.com/docs/en/google-vertex-ai_

- Prerequisites
- Sign in with Agent Platform
- Region configuration
- Set up manually
- Startup model checks
- IAM configuration
- 1M token context window
- Troubleshooting
- Additional resources

```
# Set your project ID
```

## Run Claude Code programmatically
_source: https://code.claude.com/docs/en/headless_

- Basic usage
- Examples
- Next steps

```
claude -p "Find and fix the bug in auth.py" --allowedTools "Read,Edit,Bash"
```

## Hooks reference
_source: https://code.claude.com/docs/en/hooks_

- Hook lifecycle
- Configuration
- Hook input and output
- Hook events
- Prompt-based hooks
- Agent-based hooks
- Run hooks in the background
- Security considerations
- Windows PowerShell tool
- Debug hooks

```
{
```

## Automate actions with hooks
_source: https://code.claude.com/docs/en/hooks-guide_

- Set up your first hook
- What you can automate
- How hooks work
- Prompt-based hooks
- Agent-based hooks
- HTTP hooks
- Limitations and troubleshooting
- Learn more

```
{
```

## How Claude Code works
_source: https://code.claude.com/docs/en/how-claude-code-works_

- The agentic loop
- What Claude can access
- Environments and interfaces
- Work with sessions
- Stay safe with checkpoints and permissions
- Work effectively with Claude Code
- What's next

```
Fix the login bug
```

## Interactive mode
_source: https://code.claude.com/docs/en/interactive-mode_

- Keyboard shortcuts
- Commands
- Vim editor mode
- Command history
- Background Bash commands
- Queue messages while Claude works
- Prompt suggestions
- Emoji shortcodes
- Check spelling as you type
- Side questions with /btw
- Task list
- Session recap
- Wait for a usage limit to reset
- PR review status
- See also

```
{
```

## JetBrains IDEs
_source: https://code.claude.com/docs/en/jetbrains_

- Supported IDEs
- Features
- Installation
- Usage
- Configuration
- Special configurations
- Troubleshooting
- Security considerations

```
claude
```

## Customize keyboard shortcuts
_source: https://code.claude.com/docs/en/keybindings_

- Configuration file
- Contexts
- Available actions
- Keystroke syntax
- Unbind default shortcuts
- Reserved shortcuts
- Terminal conflicts
- Vim mode interaction
- Validation

```
{
```

## Set up Claude Code in a monorepo or large codebase
_source: https://code.claude.com/docs/en/large-codebases_

- What this guide covers
- Choose where to start Claude
- Layer CLAUDE.md files by directory
- Reduce what Claude reads
- Scope worktrees and file access
- Add per-directory skills
- Test structure
- Running tests
- Test utilities
- Patterns
- Centralize conventions when layering stops scaling
- Put it together
- Scope and plan changes that span packages
- Next steps

```
monorepo/
```

## Legal and compliance
_source: https://code.claude.com/docs/en/legal-and-compliance_

- Legal agreements
- Compliance
- Usage policy
- Security and trust

## Other LLM gateways
_source: https://code.claude.com/docs/en/llm-gateway_

- What a gateway provides
- Roll out a gateway
- Subscriptions and gateways
- Related pages

## Connect Claude Code to an LLM gateway
_source: https://code.claude.com/docs/en/llm-gateway-connect_

- Check for an existing configuration
- Configure Claude Code yourself
- Configure each surface
- Additional configuration
- Troubleshoot gateway errors
- Related resources

```
{
```

## Gateway protocol reference
_source: https://code.claude.com/docs/en/llm-gateway-protocol_

- API formats
- Request headers
- System prompt attribution block
- Feature pass-through
- Model discovery
- Related resources

```
{
```

## Roll out an LLM gateway for your organization
_source: https://code.claude.com/docs/en/llm-gateway-rollout_

- Prerequisites
- Rollout steps
- Maintain the gateway
- Related resources

```
claude -p "Reply with one word: connected"
```

## Control MCP server access for your organization
_source: https://code.claude.com/docs/en/managed-mcp_

- Choose a pattern
- Exclusive control with managed-mcp.json
- Policy-based control with allowlists and denylists
- How restrictions appear to users
- Monitor MCP usage
- Configuration summary
- Related resources

```
{
```

## Deploy managed settings
_source: https://code.claude.com/docs/en/managed-settings_

- Deploy a managed settings file
- Choose a delivery mechanism
- How Claude Code combines managed sources
- Check that a policy is in force
- Keys only a managed source can set
- Turn telemetry off for your organization
- See also

```
{
```

## Connect Claude Code to tools via MCP
_source: https://code.claude.com/docs/en/mcp_

- What you can do with MCP
- Find and build MCP servers
- Installing MCP servers
- MCP installation scopes
- Practical examples
- Authenticate with remote MCP servers
- Add MCP servers from JSON configuration
- Import MCP servers from Claude Desktop
- Use MCP servers from claude.ai
- Use Claude Code as an MCP server
- MCP output limits and warnings
- Tool input schemas with a root-level combinator
- Tools with invalid input schemas
- Require approval for a specific tool
- Respond to MCP elicitation requests
- Use MCP resources
- Scale with MCP tool search
- Use MCP prompts as commands
- Managed MCP configuration

```
# Basic syntax
```

## Connect to MCP servers
_source: https://code.claude.com/docs/en/mcp-quickstart_

- Before you begin
- Add and verify a server
- Where servers are saved
- Change server scope
- Additional MCP server examples
- Edit .mcp.json directly
- Connect from other surfaces
- Troubleshooting
- Next steps

```
claude mcp remove claude-code-docs --scope local
```

## How Claude remembers your project
_source: https://code.claude.com/docs/en/memory_

- CLAUDE.md vs auto memory
- CLAUDE.md files
- Claude Code
- Auto memory
- View and edit with `/memory`
- Troubleshoot memory issues
- Related resources

```
See @README for project overview and @package.json for available npm commands for this project.
```

## Claude Code on Microsoft Foundry
_source: https://code.claude.com/docs/en/microsoft-foundry_

- Prerequisites
- Setup
- Azure RBAC configuration
- Troubleshooting
- Additional resources

```
export ANTHROPIC_FOUNDRY_API_KEY=your-azure-api-key
```

## Claude Code on mobile
_source: https://code.claude.com/docs/en/mobile_

- Get the app
- Work from your phone
- Limitations
- Related resources

## Model configuration
_source: https://code.claude.com/docs/en/model-config_

- Available models
- Restrict model selection
- Organization default model
- Organization effort limits
- Special model behavior
- Context window and auto-compaction
- Checking your current model
- Add a custom model option
- Environment variables

```
claude --model opus
```

## Monitoring
_source: https://code.claude.com/docs/en/monitoring-usage_

- Quick start
- Administrator configuration
- Configuration details
- Available metrics and events
- Interpret metrics and events data
- Audit security events
- Backend considerations
- Service information
- ROI measurement resources
- Security and privacy
- Monitor Claude Code on Amazon Bedrock

```
# 1. Enable telemetry
```

## Enterprise network configuration
_source: https://code.claude.com/docs/en/network-config_

- Proxy configuration
- CA certificate store
- Custom CA certificates
- mTLS authentication
- Verify your configuration
- Apply network settings to background agents
- Streaming idle watchdogs
- Network access requirements
- Additional resources

```
# HTTPS proxy (recommended)
```

## Output styles
_source: https://code.claude.com/docs/en/output-styles_

- Built-in output styles
- Change your output style
- Create a custom output style
- How output styles work
- Comparisons to related features
- Related resources

```
{
```

## Overview
_source: https://code.claude.com/docs/en/overview_

- Get started
- What you can do
- Use Claude Code everywhere
- Next steps

## Choose a permission mode
_source: https://code.claude.com/docs/en/permission-modes_

- Available modes
- Common setups
- Switch permission modes
- Auto-approve file edits with acceptEdits mode
- Analyze before you edit with plan mode
- Allow only pre-approved tools with dontAsk mode
- Skip all checks with bypassPermissions mode
- Protected paths
- Critical paths
- See also

```
{
```

## Configure permissions
_source: https://code.claude.com/docs/en/permissions_

- Permission system
- Manage permissions
- Permission modes
- Permission rule syntax
- Tool-specific permission rules
- Extend permissions with hooks
- Working directories
- How permissions interact with sandboxing
- Managed settings
- Settings precedence
- Project allow rules and workspace trust
- Example configurations
- See also

```
{
```

## Platforms and integrations
_source: https://code.claude.com/docs/en/platforms_

- Where to run Claude Code
- Connect your tools
- Work when you are away from your terminal
- Related resources

## Constrain plugin dependency versions
_source: https://code.claude.com/docs/en/plugin-dependencies_

- Why constrain dependency versions
- Declare a dependency with a version constraint
- Bundle plugins for a team
- Depend on a plugin from another marketplace
- Test a plugin and its dependency locally
- Tag plugin releases for version resolution
- How constraints interact
- Enable or disable a plugin with dependencies
- Remove orphaned auto-installed dependencies
- Resolve dependency errors
- See also

```
{
```

## Recommend your plugin from your CLI
_source: https://code.claude.com/docs/en/plugin-hints_

- How it works
- Emit the hint
- Choose where to emit
- What the user sees
- Hint format
- Requirements
- Get your plugin into the official marketplace
- See also

```
─────────────────────────────────────────────────────────────
```

## Create and distribute a plugin marketplace
_source: https://code.claude.com/docs/en/plugin-marketplaces_

- Overview
- Walkthrough: create a local marketplace
- Create the marketplace file
- Marketplace schema
- Plugin entries
- Plugin sources
- Host and distribute marketplaces
- Validation and testing
- Manage marketplaces from the CLI
- Troubleshooting
- See also

```
{
```

## Recommend plugins for your org
_source: https://code.claude.com/docs/en/plugin-relevance_

- How it works
- Add relevance to a plugin entry
- Field reference
- Enable suggestions in managed settings
- What the user sees
- Validate your marketplace
- See also

```
{
```

## Create plugins
_source: https://code.claude.com/docs/en/plugins_

- When to use plugins vs standalone configuration
- Quickstart
- Develop a plugin in your skills directory
- Plugin structure overview
- Develop more complex plugins
- Convert existing configurations to plugins
- Next steps

```
claude plugin init my-tool
```

## Plugins reference
_source: https://code.claude.com/docs/en/plugins-reference_

- Plugin components reference
- Plugin installation scopes
- Skills-directory plugins
- Plugin manifest schema
- Plugin caching and file resolution
- Plugin directory structure
- CLI commands reference
- Debugging and development tools
- Distribution and versioning reference
- See also

```
skills/
```

## How Claude Code uses prompt caching
_source: https://code.claude.com/docs/en/prompt-caching_

- How the cache is organized
- Actions that invalidate the cache
- Actions that keep the cache
- Cache lifetime
- Cache scope
- Check cache performance
- Subagents and the cache
- Disable prompt caching
- Related resources

## Prompt library
_source: https://code.claude.com/docs/en/prompt-library_

- What makes these prompts work
- Where these come from
- Related resources

```
add rate limiting to the public API and make sure existing tests still pass
```

## Quickstart
_source: https://code.claude.com/docs/en/quickstart_

- Before you begin
- Step 1: Install Claude Code
- Step 2: Log in to your account
- Step 3: Start your first session
- Step 4: Ask your first question
- Step 5: Make your first code change
- Step 6: Use Git with Claude Code
- Step 7: Fix a bug or add a feature
- Step 8: Test out other common workflows
- Essential commands
- Pro tips for beginners
- What's next?
- Getting help

```
claude --version
```

## Continue local sessions from any device with Remote Control
_source: https://code.claude.com/docs/en/remote-control_

- Requirements
- Start a Remote Control session
- Connection and security
- Trusted Devices
- Remote Control vs Claude Code on the web
- Mobile push notifications
- Limitations
- Troubleshooting
- Choose the right approach
- Related resources

```
claude remote-control --verbose
```

## Automate work with routines
_source: https://code.claude.com/docs/en/routines_

- Example use cases
- Create a routine
- Configure triggers
- Manage routines
- Usage and limits
- Troubleshooting
- Related resources

```
/schedule tomorrow at 9am, summarize yesterday's merged PRs
```

## Choose a sandbox environment
_source: https://code.claude.com/docs/en/sandbox-environments_

- Compare sandboxing approaches
- Choose an approach
- Sandboxed Bash tool
- Sandbox runtime
- Dev containers
- Custom container
- Virtual machine
- Claude Code on the web
- Enforce isolation across an organization
- See also

```
mkdir -p ~/.claude && echo '{}' > ~/.claude.json
```

## Configure the sandboxed Bash tool
_source: https://code.claude.com/docs/en/sandboxing_

- Get started
- Configure sandboxing
- How sandboxing works
- How sandboxing relates to permissions and permission modes
- Configure the sandbox for your organization
- Troubleshooting
- Limitations
- See also

```
{
```

## Run prompts on a schedule
_source: https://code.claude.com/docs/en/scheduled-tasks_

- Compare scheduling options
- Run a prompt repeatedly with /loop
- Set a one-time reminder
- Manage scheduled tasks
- How scheduled tasks run
- Cron expression reference
- Disable scheduled tasks
- Limitations

```
/loop 5m check if the deployment finished and tell me what happened
```

## Security
_source: https://code.claude.com/docs/en/security_

- How we approach security
- Protect against prompt injection
- MCP security
- IDE security
- Cloud execution security
- Security best practices
- Related resources

## Catch security issues as Claude writes code
_source: https://code.claude.com/docs/en/security-guidance_

- Prerequisites
- Install the plugin
- What the plugin checks
- Add your own rules
- Usage cost
- Disable or uninstall
- How the plugin integrates with Claude Code
- How this fits with other security tools
- Troubleshooting
- Related resources

```
/plugin install security-guidance@claude-plugins-official
```

## Self-hosted environments
_source: https://code.claude.com/docs/en/self-hosted-environments_

- How self-hosted environments work
- Availability and limitations
- Why self-host
- Environments, runners, and sessions
- What stays on your infrastructure
- Get started

## Customize sessions in self-hosted environments
_source: https://code.claude.com/docs/en/self-hosted-environments-configuration_

- Wrapper scripts
- Lifecycle hooks
- On-demand runners
- MCP servers
- Prompt sessions to push their work
- Permissions and tool approval
- What's next

```
claude self-hosted-runner --environment-secret-file /etc/claude/environment-secret --exec-path /etc/claude/session-wrapper.sh
```

## Deploy self-hosted environments to production
_source: https://code.claude.com/docs/en/self-hosted-environments-deploy_

- Harden your deployment
- Network requirements
- Configure git
- Build the runner image
- Size CPU and memory for sessions
- Kubernetes
- Docker Compose
- Shutdown timing
- Keep the base directory and capacity identical across runners
- Reuse a pre-warmed checkout
- Pin the version
- Scale the fleet
- Known issues and limitations
- Troubleshooting
- What's next

```
RUN git config --system user.name "Claude" && \
```

## Verify session identity in self-hosted environments
_source: https://code.claude.com/docs/en/self-hosted-environments-identity_

- The session token
- Verify the token
- Claims reference
- Scope derived credentials
- Related environment variables
- What's next

```
sk-ant-cc-<base64url header>.<base64url payload>.<base64url signature>
```

## Self-hosted environments quickstart
_source: https://code.claude.com/docs/en/self-hosted-environments-quickstart_

- Prerequisites
- Set up an environment and runner
- Send a follow-up message to a running session
- What's next

```
claude self-hosted-runner --help
```

## Self-hosted environments reference
_source: https://code.claude.com/docs/en/self-hosted-environments-reference_

- Runner CLI flags
- Orchestrator CLI flags
- Environment-variable-only settings
- Telemetry
- Health endpoint
- Prometheus metrics
- What's next

```
{
```

## Test self-hosted environments end to end
_source: https://code.claude.com/docs/en/self-hosted-environments-testing_

- Install the capture hook on your test runner
- Run the test loop
- Example script
- Remote test runners
- Authenticate from CI
- Create a dedicated test environment

```
{
```

## Configure server-managed settings
_source: https://code.claude.com/docs/en/server-managed-settings_

- Requirements
- Choose between server-managed and endpoint-managed settings
- Configure server-managed settings
- Settings delivery
- Platform availability
- Audit logging
- Security considerations
- See also

```
{
```

## Manage sessions
_source: https://code.claude.com/docs/en/sessions_

- Resume a session
- Name your sessions
- Use the session picker
- Branch a session
- Manage context within a session
- Export and locate session data
- See also

```
/branch try-streaming-approach
```

## Claude Code settings
_source: https://code.claude.com/docs/en/settings_

- Settings files and who they affect
- Change a setting
- Settings precedence
- Settings in cloud sessions
- What's next

```
{
```

## Example settings files
_source: https://code.claude.com/docs/en/settings-example_

- Your own settings

## Claude Code settings reference
_source: https://code.claude.com/docs/en/settings-reference_

- All settings
- Model and responses
- Permission settings
- Sandbox settings
- Memory and context
- Interface and terminal
- Git and attribution
- Hooks and automation
- Plugins and skills
- MCP
- Agents, sessions, and worktrees
- Remote, desktop, and notifications
- Authentication and providers
- Updates and versioning
- Tools
- Privacy and telemetry
- Enterprise and managed settings
- Global config settings
- See also

```
{
```

## Advanced setup
_source: https://code.claude.com/docs/en/setup_

- System requirements
- Install Claude Code
- Verify your installation
- Authenticate
- Update Claude Code
- Advanced installation options
- Uninstall Claude Code

```
claude
```

## Extend Claude with skills
_source: https://code.claude.com/docs/en/skills_

- Bundled skills
- Getting started
- Configure skills
- Additional resources
- Advanced patterns
- Pull request context
- Your task
- Environment
- Evaluate and iterate on a skill
- Share skills
- Usage
- What the visualization shows
- Troubleshooting
- Related resources

```
---
```

## Claude Code in Slack
_source: https://code.claude.com/docs/en/slack_

- Use cases
- Prerequisites
- Setting up Claude Code in Slack
- How it works
- User interface elements
- Access and permissions
- What's accessible where
- Best practices
- Troubleshooting
- Current limitations
- Related resources

## Customize your status line
_source: https://code.claude.com/docs/en/statusline_

- Set up a status line
- Build a status line step by step
- How status lines work
- Available data
- Examples
- Subagent status lines
- Tips
- Troubleshooting

```
/statusline show model name and context percentage with a progress bar
```

## Create custom subagents
_source: https://code.claude.com/docs/en/sub-agents_

- Built-in subagents
- Quickstart: create your first subagent
- Configure subagents
- Work with subagents
- Fork the current conversation
- Example subagents
- Next steps

```
---
```

## Configure your terminal for Claude Code
_source: https://code.claude.com/docs/en/terminal-config_

- Enter multiline prompts
- Enable Option key shortcuts on macOS
- Get a terminal bell or notification
- Configure tmux
- Fix Backspace deleting a whole word on Windows
- Match the color theme
- Switch to fullscreen rendering
- Paste large content
- Edit prompts with Vim keybindings
- Related resources

```
{
```

## Enterprise deployment overview
_source: https://code.claude.com/docs/en/third-party-integrations_

- Compare deployment options
- Configure proxies and gateways
- Best practices for organizations
- Next steps

## Tools reference
_source: https://code.claude.com/docs/en/tools-reference_

- Configure tools with permission rules and hooks
- Agent tool behavior
- AskUserQuestion tool behavior
- Bash tool behavior
- Edit tool behavior
- EndConversation tool behavior
- Glob tool behavior
- Grep tool behavior
- LSP tool behavior
- Monitor tool
- NotebookEdit tool behavior
- PowerShell tool
- Read tool behavior
- SendFeedback tool behavior
- Task tool availability
- WebFetch tool behavior
- WebSearch tool behavior
- Write tool behavior
- Check which tools are available
- See also

```
{
```

## Troubleshooting
_source: https://code.claude.com/docs/en/troubleshooting_

- Performance and stability
- Get more help

```
{
```

## Troubleshoot installation and login
_source: https://code.claude.com/docs/en/troubleshoot-install_

- Find your error
- Run diagnostic checks
- Common installation issues
- Login and authentication
- Still stuck

```
npm uninstall -g @anthropic-ai/claude-code
```

## Find bugs with ultrareview
_source: https://code.claude.com/docs/en/ultrareview_

- Run ultrareview from the CLI
- Pricing and free runs
- Track a running review
- Run ultrareview non-interactively
- How ultrareview compares to /code-review
- Related resources

```
/code-review ultra
```

## Voice dictation
_source: https://code.claude.com/docs/en/voice-dictation_

- Requirements
- Enable voice dictation
- Hold to record
- Tap to record and send
- Change the dictation language
- Rebind the dictation key
- Troubleshooting
- See also

```
/voice
```

## Use Claude Code in VS Code
_source: https://code.claude.com/docs/en/vs-code_

- Prerequisites
- Install the extension
- Get started
- Use the prompt box
- Customize your workflow
- Manage plugins
- Automate browser tasks with Chrome
- VS Code commands and shortcuts
- Configure settings
- Use a screen reader
- VS Code extension vs. Claude Code CLI
- Work with git
- Use third-party providers
- Security and privacy
- Fix common issues
- Uninstall the extension
- Next steps

```
Explain the logic in @auth (fuzzy matches auth.js, AuthService.ts, etc.)
```

## Get started with Claude Code on the web
_source: https://code.claude.com/docs/en/web-quickstart_

- How sessions run
- Compare ways to run Claude Code
- Connect GitHub
- Start a task
- Pre-fill sessions
- Review and iterate
- Troubleshoot setup
- Next steps

```
https://claude.ai/code?prompt=Fix%20the%20login%20bug&repositories=acme/webapp
```

## Week 13 · March 23–27, 2026
_source: https://code.claude.com/docs/en/whats-new/2026-w13_

## Week 14 · March 30 – April 3, 2026
_source: https://code.claude.com/docs/en/whats-new/2026-w14_

## Week 15 · April 6–10, 2026
_source: https://code.claude.com/docs/en/whats-new/2026-w15_

## Week 16 · April 13–17, 2026
_source: https://code.claude.com/docs/en/whats-new/2026-w16_

## Week 17 · April 20–24, 2026
_source: https://code.claude.com/docs/en/whats-new/2026-w17_

## Week 18 · April 27 – May 1, 2026
_source: https://code.claude.com/docs/en/whats-new/2026-w18_

## Week 19 · May 4–8, 2026
_source: https://code.claude.com/docs/en/whats-new/2026-w19_

## Week 20 · May 11–15, 2026
_source: https://code.claude.com/docs/en/whats-new/2026-w20_

## Week 21 · May 18–22, 2026
_source: https://code.claude.com/docs/en/whats-new/2026-w21_

## Week 22 · May 25–29, 2026
_source: https://code.claude.com/docs/en/whats-new/2026-w22_

## Week 23 · June 1–5, 2026
_source: https://code.claude.com/docs/en/whats-new/2026-w23_

## Week 24 · June 8–12, 2026
_source: https://code.claude.com/docs/en/whats-new/2026-w24_

## Week 25 · June 15–19, 2026
_source: https://code.claude.com/docs/en/whats-new/2026-w25_

## Week 26 · June 22–26, 2026
_source: https://code.claude.com/docs/en/whats-new/2026-w26_

## Week 27 · June 29 – July 3, 2026
_source: https://code.claude.com/docs/en/whats-new/2026-w27_

## Week 28 · July 6–10, 2026
_source: https://code.claude.com/docs/en/whats-new/2026-w28_

## Week 29 · July 13–17, 2026
_source: https://code.claude.com/docs/en/whats-new/2026-w29_

## Week 30 · July 20–24, 2026
_source: https://code.claude.com/docs/en/whats-new/2026-w30_

## Week 32 · August 3–7, 2026
_source: https://code.claude.com/docs/en/whats-new/2026-w32_

## Week 33 · August 10–14, 2026
_source: https://code.claude.com/docs/en/whats-new/2026-w33_

## Week 34 · August 17–21, 2026
_source: https://code.claude.com/docs/en/whats-new/2026-w34_

## What's new
_source: https://code.claude.com/docs/en/whats-new/index_

## Orchestrate subagents at scale with dynamic workflows
_source: https://code.claude.com/docs/en/workflows_

- When to use a workflow
- Run a bundled workflow
- Have Claude write a workflow
- Example workflow prompts
- How a workflow runs
- Manage runs
- Related resources

```
ultracode: audit every API endpoint under src/routes/ for missing auth checks
```

## Run parallel sessions with worktrees
_source: https://code.claude.com/docs/en/worktrees_

- Start Claude in a worktree
- Clean up worktrees
- Resume a worktree session
- How Claude Code enforces isolation
- Isolate subagents with worktrees
- Customize worktree creation
- What worktrees share with the main checkout
- Manage worktrees manually
- Non-git version control
- Troubleshooting
- See also

```
claude --worktree feature-auth
```

## Zero data retention
_source: https://code.claude.com/docs/en/zero-data-retention_

- ZDR scope
- Features disabled under ZDR
- Data retention for policy violations
- Request ZDR


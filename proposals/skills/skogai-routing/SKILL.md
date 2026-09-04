---
name: skogai-routing
description: "SkogAI routing use when authoring, reading, scaffolding, validating, listing, or explaining SKOGAI.md/CLAUDE.md router files, xml-blocks, route XML tags, or @-link routing."
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/list-xml-tags.sh *), Bash
---

<output>

- list-xml-tags.sh: !`${CLAUDE_SKILL_DIR}/scripts/list-xml-tags.sh`

</output>

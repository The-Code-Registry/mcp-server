# Agent Skills

This folder contains reusable skills for AI agents that integrate with The Code Registry MCP server.

## Available skills

- `code-registry/`: End-to-end workflow guidance for account setup, vault analysis, polling, re-analysis, and business-facing interpretation.

## Skill layout

`code-registry` includes:

- `SKILL.md`: Trigger and workflow instructions for agents
- `references/vault-lifecycle.md`: Detailed lifecycle and completion rules
- `references/result-interpretation.md`: Audience-specific interpretation guidance
- `scripts/poll_vault_status.py`: Deterministic polling helper

## Install

Copy `skills/code-registry` to your agent's local skills directory.

Common locations:

- Codex: `$CODEX_HOME/skills/`
- Claude Code: `~/.claude/skills/`
- Cursor (project-local): `.cursor/skills/`

## Polling helper usage

Use this when you want deterministic polling outside the conversational loop:

```bash
python3 skills/code-registry/scripts/poll_vault_status.py \
  --vault-id <vault_id> \
  --api-key <api_key>
```

Options:

- `--api-key-in-body`: send `api_key` in tool arguments for clients that cannot set headers
- `--timeout`: overall timeout in seconds (default `3600`)
- `--initial-delay` and `--max-delay`: exponential backoff controls
- `--json`: print final status payload as JSON

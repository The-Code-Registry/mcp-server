# Cursor Setup

If your Cursor build supports MCP, configure The Code Registry MCP server and restart Cursor.

## MCP server config

Use this config (same as `integrations/cursor/config.json`):

```json
{
  "mcpServers": {
    "coderegistry": {
      "url": "https://integrator.app.thecoderegistry.com/api/ai/router"
    }
  }
}
```

## Known Cursor limitation (`CallMcpTool` schema mismatch)

Some Cursor builds show a `CallMcpTool` schema that appears to only accept `{ server, toolName }`. In practice, Cursor can forward an `arguments` payload to the MCP tool at runtime.

Impact:

- Read-only tools may work.
- Tools that require inputs may fail validation if the agent assumes `arguments` cannot be sent.

Workaround:

- Always call The Code Registry tools with an explicit `arguments` object.
- If needed, add this instruction to your prompt: `Use the CallMcpTool with the arguments field to pass the required parameters.`

Example wrapper call shape:

```json
{
  "server": "coderegistry",
  "toolName": "create_project",
  "arguments": {
    "user_id": "<user_id>",
    "name": "My Project"
  }
}
```

## Agent skill recommendation

Install the `code-registry` agent skill so this workaround and full lifecycle instructions are part of the agent context by default.

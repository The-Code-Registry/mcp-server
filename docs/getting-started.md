# Getting Started

This guide walks you through a first analysis from account creation to results.

## Prerequisites
- MCP client (Claude Desktop, Claude API, or a custom MCP client)
- Access to the codebase (for LOCAL_AGENT) or a reachable Git/Archive URL

## Step 0: Initialize (recommended)
Send `initialize` once per session to confirm protocol compatibility.

```json
{
  "jsonrpc": "2.0",
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {}
  },
  "id": 1
}
```

## Step 0.5: Discover tools (optional)
Call `tools/list` to fetch the current tool catalog and input schemas.

```json
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "params": {},
  "id": 2
}
```

## Step 1: Create an account
Send the `create_account` request. The response returns `api_key`, `team_id`, and `user_id`.
When calling via JSON-RPC, parse `result.content[0].text` as JSON to access these fields.

## Step 2: Create a project
Create a project using the `user_id` from step 1.

## Step 3: Create a code vault (recommended: LOCAL_AGENT)
Use `source_type: LOCAL_AGENT` to keep code local and run the analysis command yourself.
The MCP server returns `next_steps.commands` with Docker commands.

## Step 4: Poll for results
Use `get-code-vault-summary` and `get-code-vault-results` until status is `ready`.
At this stage the code analysis can be retrieved and presented to the user, but the PDF reports may not have been generated yet.

## Step 5: Poll to fetch report URLs
Call `get-code-vault-reports` to retrieve snapshot and comparison report URLs. Once a full report PDF URL is returned in the response, that report is ready.
Comparison PDF reports will never be generated for the first analysis of a codebase (version 1.0.0)

## Next steps
- See `docs/api-reference.md` for all MCP actions.
- See `docs/troubleshooting.md` for common issues.

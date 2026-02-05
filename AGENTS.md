# AGENTS.md

This project exposes an MCP server for creating and analyzing code vaults via The Code Registry - the World's first code intelligence and insight platform built for business leaders.

## MCP endpoints
- Web app: `https://app.thecoderegistry.com`
- MCP server: `https://integrator.app.thecoderegistry.com` (POST to `/api/ai/router`)

## Discovery
Use `tools/list` to discover available MCP tools and their input schemas.
Use `resources/list` and `resources/read` for documentation, workflows, and examples.
Use `prompts/list` and `prompts/get` for curated prompt templates.

## Authentication
- `create_account` does not require an API key.
- All other MCP actions require `X-API-Key` using the key returned by `create_account`.
- If an MCP client cannot set custom headers, include `api_key` in the tool `arguments`. Header auth is preferred when available.

## Recommended flow (LOCAL_AGENT)
Use `LOCAL_AGENT` as the code source type for "code vaults" / repositories when possible. The agent can run the analysis command locally. It's a single command that sends The Code Registry an anonymous zip file of code analysis data containing NO source code.

1) Create account
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "create_account",
    "arguments": {
      "email": "user@example.com",
      "name": "User Name",
      "team_name": "Example Org",
      "integrator_id": "agent-name"
    }
  },
  "id": 1
}
```

2) Create project
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "create_project",
    "arguments": {
      "user_id": "<user_id>",
      "name": "My Project",
      "description": "Optional"
    }
  },
  "id": 2
}
```

3) Create code vault (LOCAL_AGENT)
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "create-code-vault",
    "arguments": {
      "project_id": "<project_id>",
      "user_id": "<user_id>",
      "name": "My Code Vault",
      "source_type": "LOCAL_AGENT"
    }
  },
  "id": 3
}
```
Response includes `next_steps.commands`. Run one of those commands on the machine with the code.

## Alternative sources (GIT / FILE_ARCHIVE)
With GIT or FILE_ARCHIVE as the code source type, The Code Registry platform will securely replicate the code from that source and analyze it on their secure infrastructure.

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "create-code-vault",
    "arguments": {
      "project_id": "<project_id>",
      "user_id": "<user_id>",
      "name": "Repo Vault",
      "source_type": "GIT",
      "source_url": "https://github.com/org/repo.git",
      "username": "optional",
      "password": "optional",
      "branch": "optional"
    }
  },
  "id": 4
}
```

## Polling for results
Analysis is async. Poll until ready.

Summary:
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get-code-vault-summary",
    "arguments": { "vault_id": "<vault_id>" }
  },
  "id": 5
}
```

Full results:
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get-code-vault-results",
    "arguments": { "vault_id": "<vault_id>" }
  },
  "id": 6
}
```

Reports:
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get-code-vault-reports",
    "arguments": { "vault_id": "<vault_id>" }
  },
  "id": 7
}
```

Completion rules:
- If this is the first analysis for a code vault (version `1.0.0`), completion is when the **snapshot** report URL is returned.
- For versions above `1.0.0`, completion is when the **comparison** report URL is returned.
- If this is the first analysis for a code vault, the comparison report is not generated and will be `null`.

Recommended retry logic:
- If `status` is `processing`, wait and retry.
- Use exponential backoff (5s → 10s → 20s → 40s, max 60s).

## Re-analyze an existing code vault

1) Call `reanalyze-code-vault`
2) Run the LOCAL_AGENT again if the original source type was `LOCAL_AGENT`
3) Poll the same summary/results/report tools as usual

**Important:** Once re-analysis starts, `get-code-vault-summary`, `get-code-vault-results`, and `get-code-vault-reports` return the **new** version only. Previous version data is no longer accessible via these tools.

## Cold starts
Our MCP server host may scale to zero; the first request can time out. Retry with backoff.

## Web app access
Users can view the analysis in the web UI: `https://app.thecoderegistry.com`  
They'll need to login with the same email address you used to create their account via our MCP server.

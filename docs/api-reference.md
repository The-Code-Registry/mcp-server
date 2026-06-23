# MCP API Reference

Complete reference for all MCP server actions.

## Base URL

```
https://integrator.app.thecoderegistry.com/api/ai/router
```

## Request Format (JSON-RPC)

All MCP requests use JSON-RPC 2.0. The server supports the following MCP methods:

- `initialize`
- `tools/list`
- `tools/call`
- `resources/list` and `resources/read`
- `prompts/list` and `prompts/get`

Example – initialize:

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

Example – list tools:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "params": {},
  "id": 2
}
```

Example – call a tool:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "create_account",
    "arguments": {
      "email": "user@example.com",
      "name": "John Doe",
      "team_name": "Acme Corp",
      "integrator_id": "claude-desktop"
    }
  },
  "id": 3
}
```

**Tool results:** `tools/call` returns a JSON-RPC result with `content`, where the first item is a text payload containing JSON for the tool response. Parse `result.content[0].text` as JSON to access fields like `credentials.api_key`.

Parsing tool results (JavaScript example):

```javascript
const response = await fetch(MCP_URL, { method: 'POST', headers, body })
const payload = await response.json()
const toolResult = JSON.parse(payload.result.content[0].text)
```

## Authentication

Most actions require authentication via the `X-API-Key` header. The API key is returned when creating an account.

**Header:**
```
X-API-Key: tcr_ai_xxxxxxxxxxxxxxxxxxxx
```

**Exception:** `create_account` does not require authentication.

---

## Tools and Arguments

Each action below is a tool name for `tools/call`. Use the listed fields as `params.arguments` when calling via JSON-RPC. The examples below are JSON-RPC requests.

## Resources and Prompts

Use MCP resources to fetch documentation and integration assets from this repository, and prompts to retrieve curated prompt templates.

Example – list resources:

```json
{
  "jsonrpc": "2.0",
  "method": "resources/list",
  "params": {},
  "id": 10
}
```

Example – read a resource:

```json
{
  "jsonrpc": "2.0",
  "method": "resources/read",
  "params": { "uri": "resources://docs/index" },
  "id": 11
}
```

Example – list prompts:

```json
{
  "jsonrpc": "2.0",
  "method": "prompts/list",
  "params": {},
  "id": 12
}
```

Example – get a prompt:

```json
{
  "jsonrpc": "2.0",
  "method": "prompts/get",
  "params": { "name": "first-analysis" },
  "id": 13
}
```

## Account Management

### create_account
Creates a new team account and returns API credentials.

**Authentication:** Not required

**Request Fields:**
- `email` (string, required) - Account owner's email address
- `name` (string, required) - Account owner's name
- `team_name` (string, required) - Team/company name
- `integrator_id` (string, optional) - Identifier for your MCP client (default: "default")
- `integrator_name` (string, optional) - Display name for your MCP client

**Response:** Returns `api_key`, `team_id`, `user_id`, and integrator info.

**Example:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "create_account",
    "arguments": {
      "email": "user@example.com",
      "name": "John Doe",
      "team_name": "Acme Corp",
      "integrator_id": "claude-desktop"
    }
  },
  "id": 1
}
```

**Notes:**
- Store the API key securely - it cannot be retrieved later
- If an account with the email already exists, you'll receive a 409 error
- The user can log into the web app at https://app.thecoderegistry.com with this email

---

### get_account
Returns team and user information for the authenticated account.

**Authentication:** Required

**Request Fields:** None

**Response:** Returns team and user metadata.

**Example:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get_account",
    "arguments": {}
  },
  "id": 2
}
```

---

### rotate_api_key
Generates a new API key and invalidates the old one.

**Authentication:** Required

**Request Fields:**
- `integrator_id` (string, optional) - New integrator ID for the key
- `integrator_name` (string, optional) - Display name for the integrator

**Response:** Returns new API key.

**Example:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "rotate_api_key",
    "arguments": {
      "integrator_id": "new-client"
    }
  },
  "id": 3
}
```

**Warning:** The old API key is immediately invalidated.

---

### delete_account
Deletes the team account and all associated data.

**Authentication:** Required

**Request Fields:**
- `confirm` (boolean, required) - Must be `true` to confirm deletion

**Response:** Confirmation of deletion with team and user IDs.

**Example:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "delete_account",
    "arguments": {
      "confirm": true
    }
  },
  "id": 4
}
```

**Warning:** This action is irreversible. All projects, vaults, and analysis data will be permanently deleted. This does not cancel paid subscriptions - handle that separately.

---

## Project Management

### create_project
Creates a new project within the team.

**Authentication:** Required

**Request Fields:**
- `user_id` (string, required) - User ID from account creation
- `name` (string, required) - Project name
- `description` (string, optional) - Project description

**Response:** Returns project details including ID and slug.

**Example:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "create_project",
    "arguments": {
      "user_id": "660e8400-e29b-41d4-a716-446655440000",
      "name": "Q4 Due Diligence",
      "description": "Tech DD for acquisition targets"
    }
  },
  "id": 5
}
```

**Notes:**
- Projects group related code vaults
- Use projects to organize by initiative (e.g., M&A deal, portfolio company)

---

### list_projects
Lists all projects for the authenticated team.

**Authentication:** Required

**Request Fields:** None

**Response:** Array of project objects with metadata.

**Example:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "list_projects",
    "arguments": {}
  },
  "id": 6
}
```

---

### get_project
Returns details for a specific project.

**Authentication:** Required

**Request Fields:**
- `project_id` (string, required) - Project ID to retrieve

**Response:** Project details including vault count and total lines.

**Example:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get_project",
    "arguments": {
      "project_id": "770e8400-e29b-41d4-a716-446655440000"
    }
  },
  "id": 7
}
```

---

### delete_project
Deletes a project and all its code vaults.

**Authentication:** Required

**Request Fields:**
- `project_id` (string, required) - Project ID to delete

**Response:** Confirmation with project ID.

**Example:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "delete_project",
    "arguments": {
      "project_id": "770e8400-e29b-41d4-a716-446655440000"
    }
  },
  "id": 8
}
```

**Warning:** All code vaults within the project will also be deleted.

---

## Code Vault Management

### create-code-vault
Creates a new code vault and initiates analysis.

**Authentication:** Required

**Request Fields:**
- `project_id` (string, required) - Project to create vault in
- `user_id` (string, required) - User ID creating the vault
- `name` (string, required) - Vault name
- `source_type` (string, required) - Source type: `LOCAL_AGENT`, `GIT`, or `FILE_ARCHIVE`
- `source_url` (string, required for GIT/FILE_ARCHIVE) - Repository or archive URL
- `username` (string, optional) - Authentication username for GIT
- `password` (string, optional) - Authentication password/token for GIT
- `branch` (string, optional) - Git branch to analyze (default: main/master)
- `description` (string, optional) - Vault description

**Response:** Vault details. For LOCAL_AGENT, includes `next_steps` with Docker commands.

**Example - LOCAL_AGENT:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "create-code-vault",
    "arguments": {
      "project_id": "770e8400-e29b-41d4-a716-446655440000",
      "user_id": "660e8400-e29b-41d4-a716-446655440000",
      "name": "Main Application",
      "source_type": "LOCAL_AGENT"
    }
  },
  "id": 9
}
```

**Example - GIT:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "create-code-vault",
    "arguments": {
      "project_id": "770e8400-e29b-41d4-a716-446655440000",
      "user_id": "660e8400-e29b-41d4-a716-446655440000",
      "name": "Main Application",
      "source_type": "GIT",
      "source_url": "https://github.com/acmecorp/app.git",
      "branch": "main"
    }
  },
  "id": 10
}
```

**Example - FILE_ARCHIVE:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "create-code-vault",
    "arguments": {
      "project_id": "770e8400-e29b-41d4-a716-446655440000",
      "user_id": "660e8400-e29b-41d4-a716-446655440000",
      "name": "Customer Upload",
      "source_type": "FILE_ARCHIVE",
      "source_url": "https://example.com/codebase.zip"
    }
  },
  "id": 11
}
```

**Notes:**
- **LOCAL_AGENT** (recommended): Keeps code on user's machine, sends only analysis results
- **GIT**: The Code Registry clones the repository securely
- **FILE_ARCHIVE**: The Code Registry downloads and analyzes the archive
- For GIT/FILE_ARCHIVE, the source URL must be accessible by The Code Registry infrastructure
- See troubleshooting docs for IP whitelisting requirements

---

### reanalyze-code-vault
Re-runs analysis for an existing code vault. This increments the vault version (for example, `1.0.0` → `1.0.1`) and starts a new analysis run using the original source type.

**Authentication:** Required

**Request Fields:**
- `vault_id` (string, required) - Vault ID to re-analyze

**Response:** Vault version info. For LOCAL_AGENT vaults, includes `next_steps` with Docker commands.

**Example:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "reanalyze-code-vault",
    "arguments": {
      "vault_id": "990e8400-e29b-41d4-a716-446655440000"
    }
  },
  "id": 15
}
```

**Notes:**
- If the original source type is `LOCAL_AGENT`, run the local agent again using the returned commands.
- After re-analysis starts, `get-code-vault-summary`, `get-code-vault-results`, and `get-code-vault-reports` return the **new** version only. Previous version data is no longer accessible via these tools.

---

### list_vaults
Lists all code vaults within a project.

**Authentication:** Required

**Request Fields:**
- `project_id` (string, required) - Project ID to list vaults from

**Response:** Array of vault objects with metadata.

**Example:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "list_vaults",
    "arguments": {
      "project_id": "770e8400-e29b-41d4-a716-446655440000"
    }
  },
  "id": 12
}
```

---

### get_vault
Returns metadata for a specific code vault.

**Authentication:** Required

**Request Fields:**
- `vault_id` (string, required) - Vault ID to retrieve

**Response:** Vault metadata including status and version info.

**Example:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get_vault",
    "arguments": {
      "vault_id": "990e8400-e29b-41d4-a716-446655440000"
    }
  },
  "id": 13
}
```

---

### delete-code-vault
Deletes a code vault and all its analysis data.

**Authentication:** Required

**Request Fields:**
- `vault_id` (string, required) - Vault ID to delete

**Response:** Confirmation with vault and project IDs.

**Example:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "delete-code-vault",
    "arguments": {
      "vault_id": "990e8400-e29b-41d4-a716-446655440000"
    }
  },
  "id": 14
}
```

---

## Analysis Results

### get-code-vault-summary
Returns high-level status and version information.

**Authentication:** Required

**Request Fields:**
- `vault_id` (string, required) - Vault ID to check

**Response:** Status, version, and timestamp.

**Status Values:**
- `queued` - Analysis is queued
- `processing` - Analysis in progress
- `ready` - Analysis complete, results available
- `failed` - Analysis failed

**Example:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get-code-vault-summary",
    "arguments": {
      "vault_id": "990e8400-e29b-41d4-a716-446655440000"
    }
  },
  "id": 15
}
```

**Polling Strategy:**
- Check status every 30-60 seconds while `processing`
- Use exponential backoff: 5s → 10s → 20s → 40s (max 60s)
- Stop polling when status is `ready` or `failed`

---

### get-code-vault-results
Returns analysis results for a vault. Response detail is plan-dependent.

**Authentication:** Required

**Request Fields:**
- `vault_id` (string, required) - Vault ID to retrieve results from

**Response:** Analysis data including:
- Summary statistics (lines, files, languages)
- High-level analysis metrics
- Additional facet-level detail for paid plans (for example detailed findings, expanded insights, and premium scoring outputs when enabled)

**Example:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get-code-vault-results",
    "arguments": {
      "vault_id": "990e8400-e29b-41d4-a716-446655440000"
    }
  },
  "id": 16
}
```

**Notes:**
- Only available when status is `ready`
- Free accounts can sync/analyze code and retrieve summary-level data (up to 100,000 total lines of code)
- Paid plans unlock more detailed result payloads and premium features
- See `docs/facets.md` for definitions of each facet key

---

### get-code-vault-reports
Returns URLs to downloadable PDF reports.

**Authentication:** Required

**Request Fields:**
- `vault_id` (string, required) - Vault ID to get report URLs for

**Response:** Report URLs and metadata:
- `snapshot_report` - Full analysis report for this version
- `comparison_report` - Comparison with previous version (null for v1.0.0)

**Example:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get-code-vault-reports",
    "arguments": {
      "vault_id": "990e8400-e29b-41d4-a716-446655440000"
    }
  },
  "id": 17
}
```

**Report Generation Timeline:**
- Reports are generated after analysis completes
- Snapshot report: Usually ready 5-15 minutes after `status: ready`
- Comparison report: Ready shortly after snapshot (not generated for v1.0.0)
- Reports are automatically emailed to the user

**Polling Strategy:**
- Poll this endpoint after `get-code-vault-summary` shows `ready`
- Check every 30 seconds until report URLs are returned
- For v1.0.0: Wait for `snapshot_report` only
- For v2.0.0+: Wait for both `snapshot_report` and `comparison_report`

---

## Full Data Access

The following tools expose raw analysis data and are available on paid plans. Verification-only (VerifyYourCode) plans do not include access to these tools. Each tool requires **exactly one of** `project_id` or `vault_id` — passing both or neither returns a `400 INVALID_SCOPE` error. When called with `project_id`, findings from all vaults in the project are aggregated and each item includes a `vault_name` field.

The authoritative tool schemas are always available live via `tools/list` against the MCP endpoint. Note that `schemas/mcp-tools.json` in this repository currently only covers `create_account` and does not reflect the full deployed tool set — treat the live `tools/list` response as the source of truth.

**Pagination convention (applies to all tools that support it):**
- `limit` — number of items to return (default: `50`, max: `200`)
- `offset` — zero-based offset for pagination (default: `0`)

---

### get-security-issues
Returns deduplicated security findings for a project or vault.

**Authentication:** Required (paid plan)

**Request Fields:**
- `project_id` (string) — aggregate across all vaults in this project
- `vault_id` (string) — single vault
- `api_key` (string, optional) — alternative to `X-API-Key` header
- `severity` (array of strings, optional) — filter by severity level, e.g. `["ERROR", "WARNING"]`
- `file` (string, optional) — substring match against file path
- `check_id` (string, optional) — exact match on check identifier
- `status` (string, optional) — filter by triage status
- `tag` (string, optional) — filter by tag
- `issue_id` (string, optional) — retrieve a specific issue by ID
- `limit` / `offset` (integer, optional) — pagination

**Example:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get-security-issues",
    "arguments": {
      "vault_id": "990e8400-e29b-41d4-a716-446655440000",
      "severity": ["ERROR"],
      "limit": 10
    }
  },
  "id": 20
}
```

**Response:**
```json
{
  "issues": [
    {
      "id": "1859c7c2-d04c-4e68-9378-bf0724c5aec8",
      "vault_id": "990e8400-e29b-41d4-a716-446655440000",
      "check_id": "python.lang.security.audit.subprocess-shell-true.subprocess-shell-true",
      "file": "function/activity_analyse.py",
      "line": 173,
      "severity": "ERROR",
      "issue_type": "code",
      "message": "Found 'subprocess' function 'check_output' with 'shell=True'...",
      "code_snippet": "        output = subprocess.check_output(codeclimate_cmd, shell=True)\n",
      "created_at": "2024-08-06T10:27:31",
      "updated_at": "2024-08-06T10:27:31",
      "triage": {
        "status": "first_viewed",
        "external_id": null,
        "external_ref": null,
        "external_url": null
      },
      "tags": []
    }
  ],
  "total": 47,
  "limit": 10,
  "offset": 0
}
```

**Notes:**
- When called with `project_id`, each issue includes `vault_name` instead of `vault_id`.

---

### get-code-smells
Returns code smell findings for a project or vault.

**Authentication:** Required (paid plan)

**Request Fields:**
- `project_id` (string) — aggregate across all vaults in this project
- `vault_id` (string) — single vault
- `api_key` (string, optional) — alternative to `X-API-Key` header
- `issue_type` (string, optional) — filter by smell type
- `file` (string, optional) — substring match against file path
- `issue_id` (string, optional) — retrieve a specific issue by ID
- `limit` / `offset` (integer, optional) — pagination

**Example:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get-code-smells",
    "arguments": {
      "vault_id": "990e8400-e29b-41d4-a716-446655440000",
      "limit": 50
    }
  },
  "id": 21
}
```

---

### get-git-history
Returns commit history for a project or vault.

**Authentication:** Required (paid plan)

**Request Fields:**
- `project_id` (string) — aggregate across all vaults in this project
- `vault_id` (string) — single vault
- `api_key` (string, optional) — alternative to `X-API-Key` header
- `author` (string, optional) — filter by author name or email
- `branch` (string, optional) — filter by branch name
- `date_from` (string, optional) — ISO 8601 start date
- `date_to` (string, optional) — ISO 8601 end date
- `limit` / `offset` (integer, optional) — pagination

**Example:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get-git-history",
    "arguments": {
      "vault_id": "990e8400-e29b-41d4-a716-446655440000",
      "date_from": "2024-01-01",
      "limit": 50
    }
  },
  "id": 22
}
```

---

### get-contributors
Returns aggregated contributor statistics for a project or vault.

**Authentication:** Required (paid plan)

**Request Fields:**
- `project_id` (string) — aggregate across all vaults in this project
- `vault_id` (string) — single vault
- `api_key` (string, optional) — alternative to `X-API-Key` header
- `author` (string, optional) — filter by author name or email
- `branch` (string, optional) — filter by branch name
- `date_from` (string, optional) — ISO 8601 start date
- `date_to` (string, optional) — ISO 8601 end date
- `limit` / `offset` (integer, optional) — pagination

**Example:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get-contributors",
    "arguments": {
      "vault_id": "990e8400-e29b-41d4-a716-446655440000"
    }
  },
  "id": 23
}
```

---

### get-components
Returns detected open-source and CMS components for a project or vault.

**Authentication:** Required (paid plan)

**Request Fields:**
- `project_id` (string) — aggregate across all vaults in this project
- `vault_id` (string) — single vault
- `api_key` (string, optional) — alternative to `X-API-Key` header
- `name` (string, optional) — substring match on component name
- `vendor` (string, optional) — substring match on vendor name
- `url` (string, optional) — substring match on component URL
- `only_outdated` (boolean, optional) — return only outdated components
- `sort_by_size` (boolean, optional) — sort results by size
- `limit` / `offset` (integer, optional) — pagination

**Example:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get-components",
    "arguments": {
      "vault_id": "990e8400-e29b-41d4-a716-446655440000",
      "only_outdated": true
    }
  },
  "id": 24
}
```

---

### get-code-iq-automated-queries
Returns trimmed Code IQ automated analyses (architecture, scalability, EOL, AI functionality, and more) for a project or vault.

**Authentication:** Required (paid plan)

**Request Fields:**
- `project_id` (string) — aggregate across all vaults in this project
- `vault_id` (string) — single vault
- `api_key` (string, optional) — alternative to `X-API-Key` header
- `analysis_key` (string, optional) — return a single analysis by key; omit to return all

**Example — all analyses:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get-code-iq-automated-queries",
    "arguments": {
      "vault_id": "990e8400-e29b-41d4-a716-446655440000"
    }
  },
  "id": 25
}
```

**Example — single analysis:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get-code-iq-automated-queries",
    "arguments": {
      "vault_id": "990e8400-e29b-41d4-a716-446655440000",
      "analysis_key": "project_architecture"
    }
  },
  "id": 26
}
```

**Notes:**
- `analysis_key: "code_score"` is **not valid** for this tool — it returns a `404` pointing to `get-the-code-score` instead. Use `get-the-code-score` for The Code Score.

---

### get-the-code-score
Returns The Code Score — a 1,000-point composite score covering security, code quality, and dependencies — for a project or vault.

**Authentication:** Required (paid plan)

**Request Fields:**
- `project_id` (string) — aggregate across all vaults in this project
- `vault_id` (string) — single vault
- `api_key` (string, optional) — alternative to `X-API-Key` header

**Example:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get-the-code-score",
    "arguments": {
      "vault_id": "990e8400-e29b-41d4-a716-446655440000"
    }
  },
  "id": 27
}
```

**Notes:**
- If the score has not been generated yet, or the plan does not include it, the response returns an empty `sections` and `priorities` with an explanatory `description`. See `docs/response-schemas.md` for the exact shape of both edge cases.

---

## Error Codes

All errors follow this format:
```json
{
  "error": {
    "message": "Human-readable error message",
    "code": "ERROR_CODE",
    "status": 400,
    "details": { ... }
  }
}
```

### Error Code Reference

| Code | Status | Description | Action |
|------|--------|-------------|--------|
| `VALIDATION_ERROR` | 400 | Missing or invalid request fields | Check request format and required fields |
| `INVALID_API_KEY` | 401 | API key is missing, invalid, or expired | Verify X-API-Key header and key validity |
| `FORBIDDEN` | 403 | Not authorized to access this resource | Ensure API key belongs to the resource's team |
| `LIMIT_EXCEEDED` | 403 | Plan restriction or usage limit reached | Upgrade account or contact support |
| `NOT_FOUND` | 404 | Resource not found | Verify resource ID and team ownership |
| `ACCOUNT_EXISTS` | 409 | Account with email already exists | Use existing account or different email |
| `CONFIG_ERROR` | 500 | Server misconfiguration | Contact support |
| `SERVER_ERROR` | 500 | Internal server error | Retry or contact support |
| `TIMEOUT` | 504 | Request timeout (cold start) | Retry with exponential backoff |

### Cold Start Handling

The MCP server may scale to zero during periods of inactivity. The first request after idle time may timeout.

**Recommended Retry Logic:**
```javascript
async function callMCP(payload, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      return await fetch(MCP_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': apiKey
        },
        body: JSON.stringify(payload)
      });
    } catch (error) {
      if (error.status === 504 && i < retries - 1) {
        await sleep(Math.pow(2, i) * 1000); // Exponential backoff
        continue;
      }
      throw error;
    }
  }
}
```

---

## Rate Limits

Current rate limits (subject to change):
- Account creation: 10 per hour per IP
- API requests: 1000 per hour per API key
- Analysis queue: 5 concurrent analyses per team (Free tier)

**Note:** Contact support@thecoderegistry.com for higher limits.

---

## Best Practices

### 1. Store API Keys Securely
- Never commit API keys to version control
- Use environment variables or secure secret management
- Rotate keys periodically using `rotate_api_key`

### 2. Use LOCAL_AGENT When Possible
- Keeps source code on user's machine
- Faster analysis start time
- Better privacy guarantees
- Only analysis metadata sent to The Code Registry

### 3. Implement Proper Polling
- Use exponential backoff
- Check `get-code-vault-summary` before fetching `get-code-vault-results`
- Don't poll more frequently than every 30 seconds
- Stop polling when status is `ready` or `failed`

### 4. Handle Errors Gracefully
- Implement retry logic for timeouts
- Present clear error messages to users
- Log errors for debugging
- Check error details for actionable information

### 5. Present Results Progressively
- Don't wait for PDF reports to show users results
- Use `get-code-vault-results` as soon as status is `ready`
- Start with summary metrics; include deeper findings when available on the user's plan
- Provide PDF links when available

---

## Frequently Asked Questions

**Q: How long does analysis take?**
A: Typically 30 minutes to 2 hours, depending on codebase size. Most analyses under 100K lines complete within 45 minutes.

**Q: Can I analyze private repositories?**
A: Yes, using:
1. LOCAL_AGENT (recommended) - no repository access needed
2. GIT with authentication credentials
3. You may need to whitelist The Code Registry's IP addresses

**Q: What happens if my API key is compromised?**
A: Use `rotate_api_key` immediately to invalidate the old key and generate a new one.

**Q: Can I analyze the same repository multiple times?**
A: Yes! Re-analyzing creates a new version (1.0.0 → 2.0.0 → ...) and generates comparison reports.

**Q: Do you support languages other than JavaScript?**
A: Yes! The Code Registry supports 30+ languages including JavaScript, TypeScript, Python, Java, C#, Go, Ruby, PHP, and more.

**Q: How is my code kept secure?**
A: 
- LOCAL_AGENT: Code never leaves your machine
- GIT/FILE_ARCHIVE: Secure, encrypted infrastructure
- All data encrypted in transit and at rest
- See security documentation for details

---

## Support

- **Email**: support@thecoderegistry.com
- **Issues**: https://github.com/The-Code-Registry/mcp-server/issues
- **Documentation**: https://github.com/The-Code-Registry/mcp-server/docs
- **Website**: https://thecoderegistry.com

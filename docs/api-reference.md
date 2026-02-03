# MCP API Reference

Complete reference for all MCP server actions.

## Base URL

```
https://integrator.app.thecoderegistry.com/api/ai/router
```

## Request Format

All requests must be JSON with the following structure:

```json
{
  "type": "mcp",
  "action": "<action_name>",
  "data": { ... }
}
```

## Authentication

Most actions require authentication via the `X-API-Key` header. The API key is returned when creating an account.

**Header:**
```
X-API-Key: tcr_ai_xxxxxxxxxxxxxxxxxxxx
```

**Exception:** `create_account` does not require authentication.

---

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
  "type": "mcp",
  "action": "create_account",
  "data": {
    "email": "user@example.com",
    "name": "John Doe",
    "team_name": "Acme Corp",
    "integrator_id": "claude-desktop"
  }
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
  "type": "mcp",
  "action": "get_account"
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
  "type": "mcp",
  "action": "rotate_api_key",
  "data": {
    "integrator_id": "new-client"
  }
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
  "type": "mcp",
  "action": "delete_account",
  "data": {
    "confirm": true
  }
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
  "type": "mcp",
  "action": "create_project",
  "data": {
    "user_id": "660e8400-e29b-41d4-a716-446655440000",
    "name": "Q4 Due Diligence",
    "description": "Tech DD for acquisition targets"
  }
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
  "type": "mcp",
  "action": "list_projects"
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
  "type": "mcp",
  "action": "get_project",
  "data": {
    "project_id": "770e8400-e29b-41d4-a716-446655440000"
  }
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
  "type": "mcp",
  "action": "delete_project",
  "data": {
    "project_id": "770e8400-e29b-41d4-a716-446655440000"
  }
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
  "type": "mcp",
  "action": "create-code-vault",
  "data": {
    "project_id": "770e8400-e29b-41d4-a716-446655440000",
    "user_id": "660e8400-e29b-41d4-a716-446655440000",
    "name": "Main Application",
    "source_type": "LOCAL_AGENT"
  }
}
```

**Example - GIT:**
```json
{
  "type": "mcp",
  "action": "create-code-vault",
  "data": {
    "project_id": "770e8400-e29b-41d4-a716-446655440000",
    "user_id": "660e8400-e29b-41d4-a716-446655440000",
    "name": "Main Application",
    "source_type": "GIT",
    "source_url": "https://github.com/acmecorp/app.git",
    "branch": "main"
  }
}
```

**Example - FILE_ARCHIVE:**
```json
{
  "type": "mcp",
  "action": "create-code-vault",
  "data": {
    "project_id": "770e8400-e29b-41d4-a716-446655440000",
    "user_id": "660e8400-e29b-41d4-a716-446655440000",
    "name": "Customer Upload",
    "source_type": "FILE_ARCHIVE",
    "source_url": "https://example.com/codebase.zip"
  }
}
```

**Notes:**
- **LOCAL_AGENT** (recommended): Keeps code on user's machine, sends only analysis results
- **GIT**: The Code Registry clones the repository securely
- **FILE_ARCHIVE**: The Code Registry downloads and analyzes the archive
- For GIT/FILE_ARCHIVE, the source URL must be accessible by The Code Registry infrastructure
- See troubleshooting docs for IP whitelisting requirements

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
  "type": "mcp",
  "action": "list_vaults",
  "data": {
    "project_id": "770e8400-e29b-41d4-a716-446655440000"
  }
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
  "type": "mcp",
  "action": "get_vault",
  "data": {
    "vault_id": "990e8400-e29b-41d4-a716-446655440000"
  }
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
  "type": "mcp",
  "action": "delete-code-vault",
  "data": {
    "vault_id": "990e8400-e29b-41d4-a716-446655440000"
  }
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
  "type": "mcp",
  "action": "get-code-vault-summary",
  "data": {
    "vault_id": "990e8400-e29b-41d4-a716-446655440000"
  }
}
```

**Polling Strategy:**
- Check status every 30-60 seconds while `processing`
- Use exponential backoff: 5s → 10s → 20s → 40s (max 60s)
- Stop polling when status is `ready` or `failed`

---

### get-code-vault-results
Returns complete analysis results including all facets and AI insights.

**Authentication:** Required

**Request Fields:**
- `vault_id` (string, required) - Vault ID to retrieve results from

**Response:** Complete analysis data including:
- Summary statistics (lines, files, languages)
- Security vulnerabilities
- Complexity metrics
- Quality scores
- License compliance
- AI-generated insights and recommendations

**Example:**
```json
{
  "type": "mcp",
  "action": "get-code-vault-results",
  "data": {
    "vault_id": "990e8400-e29b-41d4-a716-446655440000"
  }
}
```

**Notes:**
- Only available when status is `ready`
- Results can be large (100KB+) for complex codebases
- AI insights include strengths, concerns, and actionable recommendations

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
  "type": "mcp",
  "action": "get-code-vault-reports",
  "data": {
    "vault_id": "990e8400-e29b-41d4-a716-446655440000"
  }
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
| `LIMIT_EXCEEDED` | 403 | Free tier limit exceeded | Upgrade account or contact support |
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
- Check `get-code-vault-summary` before fetching full results
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
- Present AI insights and key metrics first
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

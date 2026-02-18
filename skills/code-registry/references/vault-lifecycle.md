# Vault Lifecycle Reference

Use this file when implementing or validating end-to-end code-vault workflows.

## 1. Initialization and discovery

- Optional but recommended: `initialize`
- Optional: `tools/list` to confirm currently available tools and schemas

## 2. Authentication

- `create_account` does not require API key
- All other actions require `X-API-Key`
- If client cannot set headers, include `api_key` inside `arguments`

## 3. Create and analyze (first run)

1. `create_account` (if needed)
2. `create_project`
3. `create-code-vault`
4. For LOCAL_AGENT source type, run one `next_steps.commands` command locally
5. Poll status endpoints until completion criteria are met

## 4. Polling endpoints

- `get-code-vault-summary`
- `get-code-vault-results`
- `get-code-vault-reports`

Recommended retry/backoff:

- If status is `processing`, `queued`, or report status is `generating`, retry
- Wait 5s, 10s, 20s, 40s, then cap at 60s
- Retry on transient network/server timeout to handle cold starts

## 5. Completion criteria

- Version `1.0.0` (first analysis): complete when `report.snapshot_report.url` exists
- Version `> 1.0.0` (re-analysis): complete when `report.comparison_report.url` exists

Notes:

- For first analysis, `comparison_report` is expected to be `null`
- Snapshot report can exist before comparison report on later versions; this is not complete for versions above `1.0.0`

## 6. Re-analysis

1. `reanalyze-code-vault`
2. Re-run LOCAL_AGENT command if source type is LOCAL_AGENT
3. Poll summary/results/reports as usual

Important behavior:

- During and after re-analysis, summary/results/reports endpoints expose only the newest version
- Older version payloads are not accessible from these endpoints

## 7. Failure handling

- `status: failed`: stop polling and report failure context
- Missing credentials (401/403): refresh API key path and retry
- Validation errors (400/422): correct tool arguments before retrying

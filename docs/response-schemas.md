# Response Schemas

This document provides detailed response schemas for all MCP actions. Request examples use MCP JSON-RPC (`tools/call`).

## JSON-RPC wrapper

When using MCP JSON-RPC (`tools/call`), the tool response is returned as a JSON string inside `result.content[0].text`. Parse that JSON to get the schemas below.

Example wrapper:
```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"status\":\"created\",\"team\":{\"id\":\"...\"}}"
      }
    ]
  },
  "id": 1
}
```

## create_account

Creates a new team account and returns credentials.

**Request:**
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

**Response:**
```json
{
  "status": "created",
  "team": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Acme Corp"
  },
  "user": {
    "id": "660e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com"
  },
  "credentials": {
    "api_key": "tcr_ai_xxxxxxxxxxxxxxxxxxxx",
    "type": "ai_integrator"
  },
  "integrator": {
    "id": "claude-desktop"
  }
}
```

**Important:** Store the `api_key` securely. Include it in all subsequent requests via the `X-API-Key` header.

---

## get_account

Returns team and user information for the authenticated API key.

**Request:**
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

**Response:**
```json
{
  "team": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Acme Corp"
  },
  "user": {
    "id": "660e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

---

## create_project

Creates a new project within the team.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "create_project",
    "arguments": {
      "user_id": "660e8400-e29b-41d4-a716-446655440000",
      "name": "Q4 Due Diligence",
      "description": "Tech DD for AcmeCorp acquisition"
    }
  },
  "id": 3
}
```

**Response:**
```json
{
  "project": {
    "id": "770e8400-e29b-41d4-a716-446655440000",
    "name": "Q4 Due Diligence",
    "slug": "q4-due-diligence",
    "description": "Tech DD for AcmeCorp acquisition",
    "created": "2025-02-03T10:30:00Z"
  }
}
```

---

## list_projects

Lists all projects for the authenticated team.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "list_projects",
    "arguments": {}
  },
  "id": 4
}
```

**Response:**
```json
{
  "projects": [
    {
      "id": "770e8400-e29b-41d4-a716-446655440000",
      "name": "Q4 Due Diligence",
      "slug": "q4-due-diligence",
      "description": "Tech DD for AcmeCorp acquisition",
      "created": "2025-02-03T10:30:00Z",
      "vault_count": 3
    },
    {
      "id": "880e8400-e29b-41d4-a716-446655440000",
      "name": "Portfolio Monitoring",
      "slug": "portfolio-monitoring",
      "description": "Monthly tech health checks",
      "created": "2025-01-15T08:00:00Z",
      "vault_count": 12
    }
  ]
}
```

---

## get_project

Returns details for a specific project.

**Request:**
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
  "id": 5
}
```

**Response:**
```json
{
  "project": {
    "id": "770e8400-e29b-41d4-a716-446655440000",
    "name": "Q4 Due Diligence",
    "slug": "q4-due-diligence",
    "description": "Tech DD for AcmeCorp acquisition",
    "created": "2025-02-03T10:30:00Z",
    "vault_count": 3,
    "total_lines": 450000
  }
}
```

---

## delete_project

Deletes a project and all its code vaults.

**Request:**
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
  "id": 6
}
```

**Response:**
```json
{
  "status": "deleted",
  "project_id": "770e8400-e29b-41d4-a716-446655440000"
}
```

---

## create-code-vault

Creates a new code vault and initiates analysis.

### LOCAL_AGENT Source Type (Recommended)

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "create-code-vault",
    "arguments": {
      "project_id": "770e8400-e29b-41d4-a716-446655440000",
      "user_id": "660e8400-e29b-41d4-a716-446655440000",
      "name": "AcmeCorp Main App",
      "source_type": "LOCAL_AGENT"
    }
  },
  "id": 7
}
```

**Response:**
```json
{
  "vault": {
    "id": "990e8400-e29b-41d4-a716-446655440000",
    "project_id": "770e8400-e29b-41d4-a716-446655440000",
    "version_id": "aa0e8400-e29b-41d4-a716-446655440000",
    "name": "AcmeCorp Main App",
    "created": "2025-02-03T10:35:00Z"
  },
  "next_steps": {
    "instructions": "Run one of the following commands from the root of your codebase:",
    "commands": {
      "linux_macos": "docker run -it --rm --pull always -v \"$(pwd):/code\" codeintelligenceplatform/local-code-agent:latest --web-endpoint https://app.thecoderegistry.com --project-id 770e8400-e29b-41d4-a716-446655440000 --code-vault-id 990e8400-e29b-41d4-a716-446655440000",
      "windows": "docker run -it --rm --pull always -v \"%cd%:/code\" codeintelligenceplatform/local-code-agent:latest --web-endpoint https://app.thecoderegistry.com --project-id 770e8400-e29b-41d4-a716-446655440000 --code-vault-id 990e8400-e29b-41d4-a716-446655440000"
    }
  }
}
```

### GIT Source Type

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "create-code-vault",
    "arguments": {
      "project_id": "770e8400-e29b-41d4-a716-446655440000",
      "user_id": "660e8400-e29b-41d4-a716-446655440000",
      "name": "AcmeCorp Main App",
      "source_type": "GIT",
      "source_url": "https://github.com/acmecorp/main-app.git",
      "branch": "main"
    }
  },
  "id": 8
}
```

**Response:**
```json
{
  "vault": {
    "id": "990e8400-e29b-41d4-a716-446655440000",
    "project_id": "770e8400-e29b-41d4-a716-446655440000",
    "version_id": "aa0e8400-e29b-41d4-a716-446655440000",
    "name": "AcmeCorp Main App",
    "created": "2025-02-03T10:35:00Z"
  }
}
```

---

## list_vaults

Lists all code vaults within a project.

**Request:**
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
  "id": 9
}
```

**Response:**
```json
{
  "vaults": [
    {
      "id": "990e8400-e29b-41d4-a716-446655440000",
      "name": "AcmeCorp Main App",
      "source_type": "GIT",
      "latest_version": "1.0.0",
      "status": "ready",
      "created": "2025-02-03T10:35:00Z",
      "last_analyzed": "2025-02-03T11:05:00Z"
    },
    {
      "id": "bb0e8400-e29b-41d4-a716-446655440000",
      "name": "AcmeCorp API",
      "source_type": "LOCAL_AGENT",
      "latest_version": "2.1.0",
      "status": "ready",
      "created": "2025-01-20T14:00:00Z",
      "last_analyzed": "2025-02-01T09:30:00Z"
    }
  ]
}
```

---

## get_vault

Returns metadata for a specific code vault.

**Request:**
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
  "id": 10
}
```

**Response:**
```json
{
  "vault": {
    "id": "990e8400-e29b-41d4-a716-446655440000",
    "project_id": "770e8400-e29b-41d4-a716-446655440000",
    "name": "AcmeCorp Main App",
    "source_type": "GIT",
    "source_url": "https://github.com/acmecorp/main-app.git",
    "latest_version": "1.0.0",
    "status": "ready",
    "created": "2025-02-03T10:35:00Z",
    "last_analyzed": "2025-02-03T11:05:00Z"
  }
}
```

---

## get-code-vault-summary

Returns high-level status and version information.

**Request:**
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
  "id": 11
}
```

**Response - Processing:**
```json
{
  "analysis": {
    "vault_id": "990e8400-e29b-41d4-a716-446655440000",
    "project_id": "770e8400-e29b-41d4-a716-446655440000",
    "status": "processing",
    "version": "1.0.0",
    "updated_at": "2025-02-03T10:40:00Z"
  }
}
```

**Response - Ready:**
```json
{
  "analysis": {
    "vault_id": "990e8400-e29b-41d4-a716-446655440000",
    "project_id": "770e8400-e29b-41d4-a716-446655440000",
    "status": "ready",
    "version": "1.0.0",
    "updated_at": "2025-02-03T11:05:00Z"
  }
}
```

**Status Values:**
- `queued` - Analysis is queued
- `processing` - Analysis in progress
- `ready` - Analysis complete, results available
- `failed` - Analysis failed (check vault details)

---

## get-code-vault-results

Returns complete analysis results including all facets and insights.

**Request:**
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
  "id": 12
}
```

**Response:**
```json
{
  "results": {
    "vault_id": "990e8400-e29b-41d4-a716-446655440000",
    "version": "1.0.0",
    "status": "ready",
    "summary": {
      "total_lines": 125000,
      "total_files": 842,
      "languages": {
        "JavaScript": 65000,
        "TypeScript": 35000,
        "Python": 15000,
        "CSS": 10000
      }
    },
    "security": {
      "critical": 2,
      "high": 8,
      "medium": 23,
      "low": 45,
      "vulnerabilities": [
        {
          "severity": "critical",
          "type": "SQL Injection",
          "file": "src/api/users.js",
          "line": 145,
          "description": "Unsanitized user input in SQL query"
        }
      ]
    },
    "complexity": {
      "average_complexity": 8.5,
      "high_complexity_files": 12,
      "technical_debt_hours": 320
    },
    "quality": {
      "code_quality_score": 7.2,
      "test_coverage": 68,
      "documentation_coverage": 45
    },
    "licenses": {
      "compliant": true,
      "licenses_found": ["MIT", "Apache-2.0", "ISC"]
    },
    "ai_insights": {
      "strengths": [
        "Well-structured TypeScript codebase with good type safety",
        "Modern testing framework with decent coverage"
      ],
      "concerns": [
        "Critical SQL injection vulnerability needs immediate attention",
        "High technical debt in legacy JavaScript modules",
        "Documentation coverage below industry standards"
      ],
      "recommendations": [
        "Immediately patch SQL injection in users API",
        "Migrate remaining JavaScript files to TypeScript",
        "Implement automated security scanning in CI/CD"
      ]
    }
  }
}
```

---

## get-code-vault-reports

Returns URLs to downloadable PDF reports.

**Request:**
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
  "id": 13
}
```

**Response - First Analysis (v1.0.0):**
```json
{
  "report": {
    "vault_id": "990e8400-e29b-41d4-a716-446655440000",
    "version": "1.0.0",
    "snapshot_report": {
      "url": "https://reports.thecoderegistry.com/snapshots/990e8400-e29b-41d4-a716-446655440000-1.0.0.pdf",
      "generated_at": "2025-02-03T11:10:00Z"
    },
    "comparison_report": null
  }
}
```

**Response - Subsequent Analysis (v2.0.0+):**
```json
{
  "report": {
    "vault_id": "990e8400-e29b-41d4-a716-446655440000",
    "version": "2.0.0",
    "snapshot_report": {
      "url": "https://reports.thecoderegistry.com/snapshots/990e8400-e29b-41d4-a716-446655440000-2.0.0.pdf",
      "generated_at": "2025-02-10T14:20:00Z"
    },
    "comparison_report": {
      "url": "https://reports.thecoderegistry.com/comparisons/990e8400-e29b-41d4-a716-446655440000-2.0.0-vs-1.0.0.pdf",
      "generated_at": "2025-02-10T14:25:00Z",
      "comparing": "2.0.0 vs 1.0.0"
    }
  }
}
```

**Response - Reports Not Ready:**
```json
{
  "report": {
    "vault_id": "990e8400-e29b-41d4-a716-446655440000",
    "version": "1.0.0",
    "snapshot_report": null,
    "comparison_report": null,
    "status": "generating"
  }
}
```

**Important Notes:**
- For version 1.0.0, `comparison_report` will always be `null`
- Reports are generated after analysis completes
- Poll this endpoint until both reports are available
- Reports are also automatically emailed to the user

---

## delete-code-vault

Deletes a code vault and all its analysis data.

**Request:**
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

**Response:**
```json
{
  "status": "deleted",
  "vault_id": "990e8400-e29b-41d4-a716-446655440000",
  "project_id": "770e8400-e29b-41d4-a716-446655440000"
}
```

---

## rotate_api_key

Generates a new API key for the team (invalidates the old one).

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "rotate_api_key",
    "arguments": {
      "integrator_id": "claude-desktop"
    }
  },
  "id": 15
}
```

**Response:**
```json
{
  "credentials": {
    "api_key": "tcr_ai_yyyyyyyyyyyyyyyyyyyy",
    "type": "ai_integrator",
    "name": "claude-desktop"
  }
}
```

**Warning:** The old API key is immediately invalidated. Update all clients with the new key.

---

## delete_account

Deletes the team account and all associated data.

**Request:**
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
  "id": 16
}
```

**Response:**
```json
{
  "status": "deleted",
  "team_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "660e8400-e29b-41d4-a716-446655440000",
  "warning": "Deleting an account does not cancel any paid subscription."
}
```

**Warning:** This action is irreversible. All projects, vaults, and analysis data will be permanently deleted.

---

## Error Responses

All errors follow this format:

```json
{
  "error": {
    "message": "Human-readable error message",
    "code": "ERROR_CODE",
    "status": 400,
    "details": {
      "additional": "context"
    }
  }
}
```

### Common Error Codes

#### VALIDATION_ERROR (400)
```json
{
  "error": {
    "message": "Missing fields for create_account: email, name",
    "code": "VALIDATION_ERROR",
    "status": 400,
    "details": {
      "missing_fields": ["email", "name"]
    }
  }
}
```

#### INVALID_API_KEY (401)
```json
{
  "error": {
    "message": "Invalid or expired API key",
    "code": "INVALID_API_KEY",
    "status": 401,
    "details": {
      "login_url": "https://app.thecoderegistry.com"
    }
  }
}
```

#### FORBIDDEN (403)
```json
{
  "error": {
    "message": "Not authorized to access this resource",
    "code": "FORBIDDEN",
    "status": 403
  }
}
```

#### LIMIT_EXCEEDED (403)
```json
{
  "error": {
    "message": "Team has exceeded the free tier line limit. Please upgrade to continue.",
    "code": "LIMIT_EXCEEDED",
    "status": 403,
    "details": {
      "current_lines": 250000,
      "limit": 200000,
      "upgrade_url": "https://app.thecoderegistry.com"
    }
  }
}
```

#### NOT_FOUND (404)
```json
{
  "error": {
    "message": "Vault not found or not accessible",
    "code": "NOT_FOUND",
    "status": 404
  }
}
```

#### ACCOUNT_EXISTS (409)
```json
{
  "error": {
    "message": "An account with this email already exists",
    "code": "ACCOUNT_EXISTS",
    "status": 409,
    "details": {
      "email": "user@example.com"
    }
  }
}
```

#### SERVER_ERROR (500)
```json
{
  "error": {
    "message": "Internal server error",
    "code": "SERVER_ERROR",
    "status": 500
  }
}
```

#### TIMEOUT (504)
```json
{
  "error": {
    "message": "Request timeout - server may be cold starting",
    "code": "TIMEOUT",
    "status": 504
  }
}
```

**Note:** For timeout errors (504), retry the request with exponential backoff. The server may be scaling up from zero instances.

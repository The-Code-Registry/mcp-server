<div align="center">
  <img src="assets/banner.png" alt="The Code Registry" />
  
  # The Code Registry MCP Server
  
  <p>
    <strong>Enterprise-grade code intelligence for AI assistants</strong>
  </p>
  
  <p>
    <a href="#quick-start">Quick Start</a> •
    <a href="#features">Features</a> •
    <a href="#use-cases">Use Cases</a> •
    <a href="#documentation">Documentation</a> •
    <a href="https://thecoderegistry.com">Website</a>
  </p>

  [![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-blue)](https://modelcontextprotocol.io/)
  [![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
  [![Support](https://img.shields.io/badge/Support-Email-orange)](mailto:support@thecoderegistry.com)
</div>

---

Enterprise-grade code intelligence for business leaders by The Code Registry. Now with a native, fully-featured MCP server for AI agents. Analyze codebases for due diligence, tech debt, security vulnerabilities, code quality and more - directly from Claude Desktop, Claude API, and other MCP-compatible clients.

## MCP Server URL

Use this URL when configuring any MCP-compatible client:

```
https://integrator.app.thecoderegistry.com/api/ai/router
```

## What is this?

This is a hosted MCP server that lets AI agents create accounts, manage projects, analyze code, and retrieve analysis results without leaving the conversation. It is designed for business leaders (M&A professionals, CTOs, VCs, board members) who need fast, reliable code insights and clean reports.

Any codebase can be analyzed and results can be ready in as quick as 30 minutes depending on code volume. PDF reports containing the results are automatically emailed to the user after analysis is complete, and as their AI agent you can retrieve the results as soon as they are ready, to show in your conversation with the user or to generate graphs/charts/reports with etc.

## What is MCP?

The Model Context Protocol (MCP) is an open standard that enables AI assistants to securely connect to data sources and tools. Learn more at [modelcontextprotocol.io](https://modelcontextprotocol.io/).

## MCP Protocol Support

This server supports the full MCP JSON-RPC 2.0 flow, including:

- `initialize`
- `tools/list`
- `tools/call`
- `resources/list` and `resources/read`
- `prompts/list` and `prompts/get`

## Prerequisites

- An MCP-compatible client (Claude Desktop, Claude Code, or custom implementation)
- For LOCAL_AGENT: Docker installed on your machine
- For GIT sources: Git repository URL with appropriate access
- Basic understanding of code analysis and software metrics

## Existing accounts

If the user already has a Code Registry account, they can generate an API key in the web app and use it directly via the
`X-API-Key` header (preferred). If the MCP client cannot set custom headers, pass `api_key` in tool arguments instead.

## Features

- **Zero setup**: agents can create accounts automatically, all you need is their email address, name and team/company name
- **Privacy-first**: Using the LOCAL_AGENT code source type keeps code on your machine and only sends an anonymous zip file of results
- **Comprehensive analysis**: security, complexity, languages, file types, code quality, licenses, tech debt and more
- **Executive-friendly reports**: PDF reports automatically emailed to the user, ready for non-technical stakeholders
- **Multiple sources**: local repos or folders of code, GIT repositories, or file archives

## Quick Start

### 0) Initialize (recommended)

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

### 1) Create account

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
  "id": 2
}
```

**Response:** Returns `api_key`, `team_id`, and `user_id` (inside `result.content[0].text` as JSON) - store the API key securely and include it in all subsequent requests via `X-API-Key` header.

### 2) Create project

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
  "id": 3
}
```

### 3) Create code vault (recommended: LOCAL_AGENT)

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
  "id": 4
}
```

**Response:** Includes `next_steps.commands` with Docker commands to run locally.

### 4) Poll for results

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get-code-vault-results",
    "arguments": { "vault_id": "<vault_id>" }
  },
  "id": 5
}
```

**Note:** Results are typically ready in 30 minutes to a few hours, depending on codebase size. Poll with exponential backoff.

### 5) Fetch report URLs

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get-code-vault-reports",
    "arguments": { "vault_id": "<vault_id>" }
  },
  "id": 6
}
```

**Note:** PDF reports are generated after analysis completes and are automatically emailed to the user.

### Re-analyze an existing code vault

To re-run analysis on an existing code vault:

1) Call `reanalyze-code-vault`
2) Run the LOCAL_AGENT again if the original source type was `LOCAL_AGENT`
3) Poll the same summary/results/report tools as usual

**Important:** Once re-analysis starts, `get-code-vault-summary`, `get-code-vault-results`, and `get-code-vault-reports` return the **new** version only. Previous version data is no longer accessible via these tools.

## Use Cases

### M&A Due Diligence
Quickly assess acquisition targets for technical risk, security vulnerabilities, and architecture concerns. See `examples/use-cases/due-diligence.md`.

### Tech Debt Analysis
Monitor technical debt across your portfolio and track improvements over time. See `examples/use-cases/tech-debt-analysis.md`.

### Security Audit
Identify security vulnerabilities and compliance issues before they become problems. See `examples/use-cases/security-audit.md`.

### Portfolio Monitoring
Track engineering metrics across multiple companies in your investment portfolio. See `examples/use-cases/portfolio-monitoring.md`.

## Configuration

See `integrations/` for client-specific setup:

- **Claude Desktop** - Desktop app configuration
- **Claude API** - API integration with Python/TypeScript examples
- **Cline** - VS Code extension setup
- **Cursor** - Cursor IDE integration
- **Custom agents** - Build your own MCP client

## Pricing

- **Free Tier**: Up to 200,000 lines of code
- **Registered Users**: $2 per 1,000 lines of code per month
- **Enterprise**: Contact us at [thecoderegistry.com](https://thecoderegistry.com/) for custom pricing and volume discounts

All tiers include:
- Unlimited projects and code vaults
- Full feature access
- PDF report generation
- Email notifications

## Documentation

- **Getting started**: `docs/getting-started.md` - Step-by-step walkthrough
- **API reference**: `docs/api-reference.md` - Complete action reference
- **Authentication**: `docs/authentication.md` - API key management
- **Facets glossary**: `docs/facets.md` - Definitions for analysis facets in results
- **Troubleshooting**: `docs/troubleshooting.md` - Common issues and solutions
- **Architecture**: `docs/architecture.md` - System design overview

## Why Use The Code Registry MCP Server?

**For M&A Professionals:**
- Fast technical due diligence (hours, not weeks)
- No manual code review needed
- Executive-friendly PDF reports
- Objective technical risk assessment

**For CTOs & Technical Leaders:**
- Monitor technical debt across portfolio
- Track security vulnerabilities
- Understand codebase complexity
- Make data-driven technical decisions

**For VCs & Board Members:**
- Assess technical risk in portfolio companies
- Track engineering metrics over time
- Get objective technical insights
- Support portfolio company CTOs

## Support

- **Email**: support@thecoderegistry.com
- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Website**: [thecoderegistry.com](https://thecoderegistry.com/)

## License

See [LICENSE](LICENSE) file for details.

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

<div align="center">
  <p>Built with ❤️ by <a href="https://thecoderegistry.com">The Code Registry</a></p>
  <p>The World's first code intelligence platform built for business leaders</p>
</div>

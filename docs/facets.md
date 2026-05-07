# Facet Glossary

The `get-code-vault-results` response can include a `facets` object keyed by display slugs.
Facet availability and detail depth are plan-dependent. Free tier generally returns summary-level outputs, while paid plans can return richer facet detail.
When present, each facet object also includes a `slug` field with the raw internal slug used internally in The Code Registry's system.

## Facets

- **cost-to-replicate**: Calculates the replication value of the IP based on the detected languages and a proprietary database of market rates and language statistics.
- **ai-quotient**: Proprietary code-quality metric measuring how much of the codebase could be improved by AI. Includes non-subjective code quality issues and signals from other areas (for example, security issues and outdated open-source components).
- **code-contributors**: Uses Git history to generate statistics and summaries of code contributors.
- **languages**: Calculates languages used and lines of code per language (and totals).
- **file-types**: Lists file types and total size per type.
- **opensource-components**: Detects known CMS/open-source components, their total lines of code, whether they are outdated and any licenses.
- **security**: Scans for known vulnerabilities and security issues in first and thirdparty code.
- **git-history**: Analyzes GIT history to generate stats on code changes, contributors, developer profiles and more.
- **complexity**: Uses cyclomatic complexity to calculate overall complexity, per-language and per-codebase complexity.

Notes:
- `git-history` and `code-contributors` are only available when the source type is GIT.

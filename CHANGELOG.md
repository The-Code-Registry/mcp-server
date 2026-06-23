# Changelog

## [1.0.2] - 2026-06-23

### Added
- `get-security-issues` — retrieve deduplicated security findings for a project or vault (paid plans)
- `get-code-smells` — retrieve code smell findings for a project or vault (paid plans)
- `get-git-history` — retrieve commit history for a project or vault (paid plans)
- `get-contributors` — retrieve aggregated contributor stats for a project or vault (paid plans)
- `get-components` — retrieve detected open-source/CMS components for a project or vault (paid plans)
- `get-code-iq-automated-queries` — retrieve trimmed Code IQ automated analyses (paid plans)
- `get-the-code-score` — retrieve The Code Score (1,000-point security/quality/dependencies score) for a project or vault (paid plans)

## [1.0.1] - 2026-06-02

### Changed
- Free tier now limited to 100,000 total lines of code across all vaults (previously uncapped)

## [1.0.0] - 2026-02-02

### Added
- Initial MCP server release
- `create_account` action
- `create_project` action
- `create-code-vault` with LOCAL_AGENT, GIT, FILE_ARCHIVE
- `get-code-vault-summary` action
- `get-code-vault-results` action
- `get-code-vault-reports` action

### Notes
- Hosted at integrator.app.thecoderegistry.com

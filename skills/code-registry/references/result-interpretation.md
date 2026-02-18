# Result Interpretation Reference

Use this file to convert raw code-vault outputs into decision-oriented insights.

## Audience-specific framing

## M&A / Investment committee

Lead with:

- Overall engineering risk level
- Security and compliance blockers
- Estimated effort and cost to stabilize

Add:

- Key technical debt drivers
- Team and maintainability signals
- 30/60/90 day remediation priorities

## CTO / Engineering leadership

Lead with:

- Security severity and exploitability profile
- Reliability and complexity hotspots
- Delivery drag from debt and outdated dependencies

Add:

- Recommended sequencing for remediation
- Ownership model (platform vs product teams)
- KPI suggestions for follow-up analyses

## Core facets and how to explain them

- `ai-quotient`: code quality and modernization potential signal; use for prioritizing improvement opportunities
- `security`: vulnerability counts and severity distribution; separate critical/high from medium/low
- `complexity`: maintainability pressure; connect high complexity to incident risk and slow delivery
- `opensource-components`: dependency freshness and license risk; call out unsupported/outdated packages
- `cost-to-replicate`: replacement-cost proxy for the code asset; use as context, not a standalone decision metric
- `languages` and `file-types`: portfolio composition; useful for staffing and migration planning
- `git-history` and `code-contributors` (GIT sources): concentration risk and bus-factor indicators

## Reporting pattern

Use this structure for consistent outputs:

1. Executive Summary (3-6 bullets)
2. Critical Risks (security/compliance/reliability)
3. Value and Cost Signals (quality/debt/replication cost)
4. Recommended Actions (ordered by urgency)
5. Monitoring Plan (what to re-check on next analysis)

## Interpretation guardrails

- Do not overstate confidence when source coverage is partial
- Make clear when a metric is directional vs deterministic
- Separate observed facts from inferred conclusions
- For re-analysis, compare version-over-version deltas explicitly

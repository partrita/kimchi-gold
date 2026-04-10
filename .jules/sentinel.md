## 2024-04-07 - [Security Enhancement] Enforce HTTPS in Data Fetching
**Vulnerability:** URL validation allowed the `http` scheme, creating a risk for Unencrypted Sensitive Data Transmission and Man-in-the-Middle (MitM) attacks.
**Learning:** Hardcoded allowed schemes in URL validation should exclusively permit `https` unless there is a specific, documented need for unencrypted HTTP traffic.
**Prevention:** Strictly validate `parsed_url.scheme == "https"` during all data fetching operations and remove `http` from allowed lists.

## 2024-04-07 - [Security Enhancement] GitHub Actions Permissions
**Vulnerability:** GitHub Actions workflows were lacking explicit `permissions` blocks, violating the Principle of Least Privilege.
**Learning:** Without explicit permissions, the default `GITHUB_TOKEN` might be granted broader access than required (e.g., repository write access), increasing the blast radius if an action is compromised.
**Prevention:** Always declare explicit, scoped `permissions` (e.g., `contents: read`, `issues: write`) at the top level of every `.yml` workflow file.
## 2026-04-10 - Stack Trace Leakage in Automation Scripts
**Vulnerability:** Internal error handling in automation scripts (`scripts/collect_data.py`, `scripts/analyze_outlier.py`, `scripts/generate_chart.py`) was leaking stack traces via `logger.error(..., exc_info=True)` and `traceback.print_exc()`, potentially exposing sensitive internal details in GitHub Actions logs.
**Learning:** Overly verbose logging designed for debugging during local development was left in production scripts executed in a CI/CD environment, violating the "fail securely" principle.
**Prevention:** Avoid using `exc_info=True` or `traceback.print_exc()` in non-debug logging contexts, specifically in scripts designed to execute via CI/CD platforms, ensuring error messages are descriptive but do not reveal internal implementation details.

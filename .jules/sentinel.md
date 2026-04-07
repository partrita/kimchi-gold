## 2024-04-07 - [Security Enhancement] Enforce HTTPS in Data Fetching
**Vulnerability:** URL validation allowed the `http` scheme, creating a risk for Unencrypted Sensitive Data Transmission and Man-in-the-Middle (MitM) attacks.
**Learning:** Hardcoded allowed schemes in URL validation should exclusively permit `https` unless there is a specific, documented need for unencrypted HTTP traffic.
**Prevention:** Strictly validate `parsed_url.scheme == "https"` during all data fetching operations and remove `http` from allowed lists.

## 2024-04-07 - [Security Enhancement] GitHub Actions Permissions
**Vulnerability:** GitHub Actions workflows were lacking explicit `permissions` blocks, violating the Principle of Least Privilege.
**Learning:** Without explicit permissions, the default `GITHUB_TOKEN` might be granted broader access than required (e.g., repository write access), increasing the blast radius if an action is compromised.
**Prevention:** Always declare explicit, scoped `permissions` (e.g., `contents: read`, `issues: write`) at the top level of every `.yml` workflow file.

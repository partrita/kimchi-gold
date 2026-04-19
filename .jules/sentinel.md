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

## 2024-04-11 - [Security Enhancement] SSRF Bypass via Backslash Normalization
**Vulnerability:** URL validation using `urlparse` allowed a bypass using the backslash `\` character in the domain (e.g. `https://127.0.0.1\.naver.com/`). `urlparse` treats the backslash as part of the `netloc`, passing domain suffix checks, while HTTP clients like `requests` normalize the `\` to `/`, routing the request to the IP Address `127.0.0.1` instead.
**Learning:** Checking for specific string suffixes like `.endswith(".naver.com")` after extracting components via `urllib.parse` is prone to bypasses because libraries resolving the request might parse and normalize the input differently than Python's standard `urlparse`.
**Prevention:** In addition to verifying the domain name suffix, explicitly reject any URLs that contain invalid hostname characters like `@` or `\` in the `netloc`.

## 2026-04-13 - [Security Enhancement] SSRF Bypass via Internal Ports
**Vulnerability:** URL validation did not check the requested port, allowing potential SSRF bypasses to internal services running on non-standard ports (e.g., Redis on 6379, databases on 5432, custom internal APIs on 8080) if an attacker managed to bypass domain validation.
**Learning:** Only validating the URL scheme (`https`) and domain is insufficient defense-in-depth, as attackers can specify arbitrary ports to scan or interact with internal infrastructure.
**Prevention:** Explicitly validate `parsed_url.port` and only permit standard web ports (e.g. `443` or `None` which implies the default for the scheme) during data fetching operations.

## 2026-04-14 - [Vulnerability] Connection Pool Exhaustion DoS
**Vulnerability:** `requests.get` with `stream=True` was used without a `with` context manager. When a `ValueError` was raised for exceeding the size limit (5MB), the underlying connection was not guaranteed to be released back to the pool, leading to resource exhaustion (DoS) when many requests hit the limit.
**Learning:** Reading chunked responses using `iter_content` leaves the connection open if not fully consumed. Raising exceptions before the end of the stream without explicitly closing the response leaks connections.
**Prevention:** Always wrap `requests.get(..., stream=True)` in a `with` context manager to ensure the connection is closed and released, even if an exception is raised early.

## 2024-05-24 - Content-Type validation and Timeout for Slow-Read DoS in streams
**Vulnerability:** Unintended payload processing and Slowloris-style slow-read DoS.
**Learning:** `requests.get` with `stream=True` and a max size check is vulnerable to slow-read attacks where an attacker sends data extremely slowly, exhausting server resources/connection pools, and missing `Content-Type` validation could lead to parsing non-HTML binary payloads using BeautifulSoup.
**Prevention:** To prevent unintended payload types and mitigate Slowloris-style slow-read DoS attacks, explicitly validate the `Content-Type` header (e.g., `text/html`) before reading HTTP responses and enforce a strict absolute time limit within the `requests` streaming loop.

## 2026-04-19 - [Security Enhancement] Input Validation and Length Limits for Price Data
**Vulnerability:** Extracted price data strings were cast to `float` without string length limits, and numerical validation did not account for `NaN`, `Inf`, or unfeasibly large values, posing algorithmic complexity DoS risks (e.g., extremely long float parsing) and data poisoning/logic errors downstream.
**Learning:** External inputs parsed from HTML, even those matched by a regex, must be strictly bounded in both string length before parsing and numerical range after parsing. Missing NaN/Inf checks on floats can lead to unexpected behavior in financial logic.
**Prevention:** Implement strict length limits (e.g., 50 characters) on extracted strings before type conversion to prevent long-string processing overhead. Enhance numeric validation to explicitly reject `math.isnan`, `math.isinf`, and logically excessive values (e.g., > 1,000,000,000) to ensure data integrity and prevent downstream errors.

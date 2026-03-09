## 2026-03-09 - [Secure Web Scraping & Error Sanitization]
**Vulnerability:** Information leakage through verbose error messages and potential SSRF due to unvalidated scrap targets.
**Learning:** Even in simple data-gathering tools, raw exception details (like requests.HTTPError) can leak sensitive internal URLs or proxy configurations. Additionally, fetching from arbitrary URLs passed to scraping functions can lead to SSRF if the inputs are ever influenced by external sources.
**Prevention:** Always wrap external calls in try-except blocks that sanitize output for end-users. Validate domains for all outgoing requests against an allowlist, and enforce strict response size limits to prevent Resource Exhaustion (DoS).

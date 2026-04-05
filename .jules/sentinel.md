## 2024-05-24 - [SSRF Protection]
**Vulnerability:** Server-Side Request Forgery (SSRF) risk in `extract_price_from_naver_finance` due to unvalidated `target_url` parameter being passed directly to `requests.get`.
**Learning:** Functions designed to fetch data from specific external sources must validate the URL scheme and domain to prevent arbitrary requests to internal or external services.
**Prevention:** Implement URL validation using `urllib.parse.urlparse` to strictly enforce allowed schemes (`http`, `https`) and domains (e.g., `naver.com` and its subdomains) before making HTTP requests.

## 2024-05-24 - [SSRF Open Redirect Bypass Protection]
**Vulnerability:** Server-Side Request Forgery (SSRF) bypass risk in `extract_price_from_naver_finance` where `requests.get` implicitly follows HTTP redirects.
**Learning:** Even if the initial URL domain is strictly validated, following HTTP redirects by default can allow an attacker to bypass domain validation if the allowed domain contains an open redirect vulnerability, directing the request to unauthorized domains or internal network targets.
**Prevention:** Explicitly disable HTTP redirects by passing `allow_redirects=False` to `requests.get` (or similar HTTP clients) and validate the response status code, ensuring no redirection occurs when fetching data from external URLs.

## 2024-05-24 - [SSRF Bypass via URL Parsing Discrepancies]
**Vulnerability:** Server-Side Request Forgery (SSRF) bypass in `extract_price_from_naver_finance` caused by passing URLs containing `@` (e.g., `http://127.0.0.1\@naver.com/`).
**Learning:** Python's `urllib.parse.urlparse` and the HTTP client library (`urllib3` inside `requests`) parse URLs differently. When an attacker supplies a URL with basic auth characters (`@`), `urlparse` may identify the hostname as the part after the `@` (e.g., `naver.com`), satisfying domain allowlists. However, `urllib3` may treat the part before the `@` as the host (e.g., `127.0.0.1`), allowing requests to unauthorized destinations.
**Prevention:** Explicitly block the `@` character in the `netloc` component of the parsed URL to prevent discrepancies between URL parsing libraries from being exploited to bypass domain validation.
## 2026-04-05 - [GitHub Actions Script Injection Protection]
**Vulnerability:** Script injection vulnerability in `.github/workflows/Daily_collect.yml` where action output was directly interpolated into `github-script` using `${{ }}`.
**Learning:** Direct interpolation of unsanitized or dynamic output into inline scripts can allow attackers to break out of string context (e.g., using backticks) and execute arbitrary code with workflow privileges.
**Prevention:** Always pass dynamic data to scripts via environment variables (e.g., `process.env`) instead of direct string interpolation.

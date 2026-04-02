## 2024-05-24 - [SSRF Protection]
**Vulnerability:** Server-Side Request Forgery (SSRF) risk in `extract_price_from_naver_finance` due to unvalidated `target_url` parameter being passed directly to `requests.get`.
**Learning:** Functions designed to fetch data from specific external sources must validate the URL scheme and domain to prevent arbitrary requests to internal or external services.
**Prevention:** Implement URL validation using `urllib.parse.urlparse` to strictly enforce allowed schemes (`http`, `https`) and domains (e.g., `naver.com` and its subdomains) before making HTTP requests.

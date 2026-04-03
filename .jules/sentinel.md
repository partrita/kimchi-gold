## 2024-05-24 - [SSRF Protection]
**Vulnerability:** Server-Side Request Forgery (SSRF) risk in `extract_price_from_naver_finance` due to unvalidated `target_url` parameter being passed directly to `requests.get`.
**Learning:** Functions designed to fetch data from specific external sources must validate the URL scheme and domain to prevent arbitrary requests to internal or external services.
**Prevention:** Implement URL validation using `urllib.parse.urlparse` to strictly enforce allowed schemes (`http`, `https`) and domains (e.g., `naver.com` and its subdomains) before making HTTP requests.

## 2024-05-24 - [SSRF Open Redirect Bypass Protection]
**Vulnerability:** Server-Side Request Forgery (SSRF) bypass risk in `extract_price_from_naver_finance` where `requests.get` implicitly follows HTTP redirects.
**Learning:** Even if the initial URL domain is strictly validated, following HTTP redirects by default can allow an attacker to bypass domain validation if the allowed domain contains an open redirect vulnerability, directing the request to unauthorized domains or internal network targets.
**Prevention:** Explicitly disable HTTP redirects by passing `allow_redirects=False` to `requests.get` (or similar HTTP clients) and validate the response status code, ensuring no redirection occurs when fetching data from external URLs.

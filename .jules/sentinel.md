[Output truncated for brevity]

lidating the URL scheme (`https`) and domain is insufficient defense-in-depth, as attackers can specify arbitrary ports to scan or interact with internal infrastructure.
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

## 2026-05-09 - [Security Enhancement] Fail-fast Content-Length Validation and Thread Timeouts
**Vulnerability:** A missing fail-fast `Content-Length` check meant the application would start processing chunks of an excessively large payload before aborting, slightly increasing overhead. Concurrently, missing timeouts on `future.result()` calls for threaded network requests could lead to infinite blocking if a request stalled.
**Learning:** Checking payload size only during stream iteration allows attackers to initiate malicious processing, consuming partial resources. Additionally, threads handling network I/O must always have hard timeouts on their results to prevent process hanging.
**Prevention:** Implement a fail-fast mechanism by checking the `Content-Length` HTTP header before stream processing begins, and always enforce explicit timeouts on `.result()` when fetching data via `ThreadPoolExecutor`.
## 2026-05-15 - [Security Enhancement] Robust Fail-fast Content-Length Validation\n**Vulnerability:** A logic error in the fail-fast `Content-Length` validation incorrectly caught parsing exceptions (`ValueError`) and unconditionally raised a new `ValueError`, turning malformed headers into a self-inflicted DoS vulnerability instead of falling back to the secondary stream size check.\n**Learning:** Exception handling for malformed input during security validation must be carefully isolated so it doesn't inadvertently trigger the security violation handler and cause a DoS.\n**Prevention:** When parsing inputs for fail-fast limits, catch parsing errors cleanly and default to safe fallback values (e.g., `None`), allowing secondary defense-in-depth mechanisms to handle the validation.

## 2026-04-26 - [Security Enhancement] SSRF Bypass via Parsing Discrepancies and Homograph Attacks
**Vulnerability:** URL validation only checked if the hostname `endswith(".naver.com")`, but did not strictly validate the characters composing the hostname itself. This lack of character validation opened the door to advanced SSRF bypasses such as IDNA homograph attacks (e.g., using `naver。com` where `。` normalizes to `.`), zero bytes, newline injections, or other parsing discrepancies between `urlparse` and the underlying HTTP client.
**Learning:** Only validating the suffix of a hostname is insufficient against advanced bypass techniques. Different libraries may normalize or parse unusual characters in hostnames differently, leading to cases where a validation check passes but the actual request is routed to an attacker-controlled or unintended destination.
**Prevention:** In addition to validating the domain suffix, enforce a strict allowlist of permitted characters for the `hostname` (e.g., `^[a-zA-Z0-9.-]+$`) using regex before performing further validation. This prevents malicious characters from exploiting parsing discrepancies.

## 2026-04-30 - [Security Enhancement] Prevent Algorithmic Complexity DoS in Number Sequences
**Vulnerability:** Numerical thresholds such as step sizes and bounds (`threshold_step`) in loops or generator functions like `numpy.arange` were passed directly without being validated, making them vulnerable to `ZeroDivisionError` (if step=0) or an Algorithmic Complexity DoS condition by creating immense iterations (if step is an extremely small fraction).
**Learning:** Functions orchestrating loops, ranges, and array generation should not blindly trust input variables passed to them without validation, especially if those variables could be user-controlled CLI parameters.
**Prevention:** Strictly enforce mathematical bounds (`> 0`) on parameter types like step increments and array dimensions, immediately rejecting negative or zero values.
## 2025-04-29 - [Missing CLI Parameter Validation]
**Vulnerability:** Unbounded CLI parameters and potential for ZeroDivisionError in `optimal_threshold.py` and `backtest.py` via an initial investment <= 0 or extreme float ranges.
**Learning:** External parameters, like CLI arguments, can be crafted to consume excessive memory or divide-by-zero, leading to application crashes.
**Prevention:** Implement strict boundary checks on numeric inputs to prevent both memory exhaustion via unbounded arrays and fatal errors like ZeroDivisionError.

## 2026-05-18 - [Security Enhancement] Enforce Strict Connection Timeouts
**Vulnerability:** External data fetching used a single integer timeout (`timeout=10`) in `requests.get()`. This single value applies to both the connection phase and the read phase. A malicious or uncooperative server could act as a tarpit, accepting the TCP connection but never responding, tying up client resources for the full duration or longer if not carefully managed.
**Learning:** Using a single timeout value in `requests` can lead to resource exhaustion if many connections hang during the initial handshake. Best practice dictates separating connection and read timeouts.
**Prevention:** Always use a tuple for the `timeout` parameter (e.g., `timeout=(3.0, 10.0)`) to ensure the application fails fast if a connection cannot be quickly established, thereby preventing Denial of Service (DoS) via resource exhaustion.

## 2026-05-20 - [Security Enhancement] Enforce math.isfinite on Float CLI Parameters
**Vulnerability:** Float CLI parameters (e.g., `min_threshold`, `max_threshold`, `buy_threshold`, `sell_threshold`) lacked `math.isfinite` validation. When passed non-finite values like `NaN` or `Inf`, the logic downstream produced erratic outcomes or application crashes (such as `ValueError: arange: cannot compute length` during sequence generation in `numpy`).
**Learning:** Python's `float` type natively accepts `NaN` and `Inf`. When these values bypass initial validation and propagate to mathematical operations or sequence generators (like `numpy.arange`), they can lead to unhandled exceptions, logic errors, or DoS conditions.
**Prevention:** Always validate user-provided float inputs using `math.isfinite()` to ensure they are concrete numeric values before executing dependent operations.

## 2026-05-07 - [Security Enhancement] Implement Automated Security Scanning in CI/CD
**Vulnerability:** The application lacked automated security scanning in its CI/CD pipeline. This meant that new vulnerabilities (e.g., insecure coding practices or vulnerable dependencies) could easily be introduced into the `main` branch without detection, increasing the risk of deployment.
**Learning:** Security must be integrated directly into the development workflow as a defense-in-depth measure. Relying solely on manual reviews or ad-hoc scans is insufficient for maintaining a strong security posture. Continuous security scanning ensures that every change is automatically evaluated against known vulnerability databases and secure coding standards.
**Prevention:** Implement a GitHub Actions workflow with restricted permissions (`contents: read`) that automatically runs tools like `bandit` for Static Application Security Testing (SAST) and `pip-audit` for dependency vulnerability scanning on every pull request and push to the main branch.

## 2026-05-12 - [Security Enhancement] Prevent Algorithmic Complexity DoS during Content-Length Parsing
**Vulnerability:** The application parsed the `Content-Length` HTTP header using Python's built-in `int()` function without placing any upper bound on the length of the string to parse.
**Learning:** Calling `int()` on extremely long strings in Python can cause the interpreter to consume significant CPU and memory resources, leading to an Algorithmic Complexity Denial-of-Service (DoS) condition.
**Prevention:** To prevent Algorithmic Complexity DoS from Python's `int()` parsing, enforce strict string length bounds (e.g., `<= 20` characters) before converting HTTP headers like `Content-Length` to integers. Negative sizes should also be rejected to prevent downstream bypasses.

## 2026-05-24 - [Security Enhancement] Prevent Algorithmic Complexity DoS during Date Parsing
**Vulnerability:** The application parsed the `start-date` CLI parameter using `datetime.strptime()` without placing any upper bound on the length of the string to parse.
**Learning:** Calling `datetime.strptime()` on extremely long strings in Python can cause the interpreter to consume significant CPU and memory resources, leading to an Algorithmic Complexity Denial-of-Service (DoS) condition.
**Prevention:** To prevent Algorithmic Complexity DoS from Python's string parsing in `datetime`, enforce strict string length bounds (e.g., `<= 20` characters) before converting parameters like `start-date` to datetime objects.

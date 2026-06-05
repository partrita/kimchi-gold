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

## 2026-05-24 - [Security Enhancement] Add Audit Logging for Security Events
**Vulnerability:** The codebase implemented robust defenses against SSRF and DoS (validating URL schemes, preventing redirects, checking Content-Length and Content-Type) by silently raising ValueErrors. However, these mitigations lacked an audit trail, meaning that while attacks were stopped, they were not logged or flagged, preventing administrators from observing or reacting to active attacks or misconfigurations.
**Learning:** A security mitigation that simply blocks an action without logging it is incomplete. "Silent" mitigations obscure attack patterns and hinder incident response, as there is no record of the thwarted attempt or its context.
**Prevention:** Whenever a security control blocks an action or input (e.g., rejecting an SSRF attempt or stopping a DoS payload), explicitly log the event (e.g., using `logger.warning("[SECURITY] ...")`) before raising an exception or returning an error. This ensures security event observability.

## 2025-05-20 - Prevent Information Leakage in Error Responses
**Vulnerability:** Raw exception messages (e.g., `collection_error`, `file_write_error`) were appended to user-facing `ValueError`, `IOError`, and `print()` statements in `price_fetcher.py` and `data_collector.py`.
**Learning:** Exposing raw exceptions can inadvertently leak sensitive system information, such as file paths, internal logic states, or network configurations, aiding attackers in reconnaissance.
**Prevention:** To prevent information leakage, securely log the raw exception details internally using a logging framework (`logger.error`), but raise or return generic, user-safe error messages (e.g., "시스템 로그를 확인해주세요.") to the end user.

## 2026-05-21 - Explicitly Enforce TLS Verification
**Vulnerability:** MitM vulnerability via disabled TLS verification
**Learning:** Relying on default library parameters for critical security mechanisms leaves the application vulnerable if defaults are overridden (e.g., globally via env vars) or accidentally changed.
**Prevention:** Explicitly specify security-critical parameters like `verify=True` in `requests` calls to ensure secure defaults are enforced.

## 2026-05-24 - [Security Enhancement] Prevent Information Leakage in CLI Tools
**Vulnerability:** The CLI tools (`backtest.py`, `optimal_threshold.py`, `chart_generator.py`) printed raw exception details and absolute internal server paths (e.g., `Path.cwd()`) directly to standard output upon failure.
**Learning:** Directly printing unhandled exceptions or internal system states to the console in CLI tools or scripts exposes sensitive implementation details (CWE-209), which could be useful to an attacker if the CLI tool's output is inadvertently logged or returned to an unauthorized user in an automated environment (like CI/CD or a wrapper API).
**Prevention:** In CLI scripts, route detailed errors and context (such as file paths and exception stacks) to the internal logging framework using `logger.exception()` or `logger.error()`, and output only generic, safe error messages (e.g., "Error: 시스템 로그를 확인해주세요.") to the user-facing console.

## 2026-05-31 - [Security Enhancement] Secure CI/CD Dependency Installation
**Vulnerability:** The `.github/workflows/publish-website.yml` workflow installed Python dependencies (`pandas`, `plotly`, `jupyter`, `pyyaml`) dynamically via `pip install` without version pinning or vulnerability scanning, making the workflow susceptible to supply chain attacks (e.g., dependency confusion or malicious updates).
**Learning:** Dependencies installed on the fly in CI/CD pipelines without being tracked in the main dependency manifest (`pyproject.toml`) bypass automated security checks (like `pip-audit`) and lack reproducibility.
**Prevention:** To prevent supply chain attacks in CI/CD, all dependencies (including those used for auxiliary tasks like building documentation or websites) must be explicitly declared in the project's dependency manifest (e.g., as an optional dependency group). Update CI scripts to install from this defined group (e.g., `pip install .[website]`) and ensure security scanners (e.g., `pip-audit`) are configured to scan all extras (`--all-extras`).

## 2026-05-30 - [Security Enhancement] Prevent Information Leakage in CLI Tools
**Vulnerability:** The chart generator CLI script and library printed the absolute internal file paths of the generated charts directly to standard output upon success.
**Learning:** Directly printing absolute file paths to the console in CLI tools or scripts exposes internal system details (CWE-209), which could be useful to an attacker for reconnaissance.
**Prevention:** Output only generic or relative filenames (e.g. `kimchi_gold_price_recent_12months.png`) to the user-facing console, while routing detailed internal context (like absolute file paths) to the logging framework using `logger.info()` for auditing purposes.

## YYYY-MM-DD - [Add Workflow Timeouts]
**Vulnerability:** Missing timeout configurations in GitHub Actions workflows.
**Learning:** Without explicit timeouts, compromised dependencies or malicious PRs can intentionally hang CI runners (e.g., infinite loops or cryptomining tarpits), exhausting the repository's GitHub Actions compute quota and causing a Denial of Service (DoS) for the CI/CD pipeline.
**Prevention:** Always define a job-level `timeout-minutes` configuration (e.g., `timeout-minutes: 10`) in all GitHub Actions workflows to enforce strict execution time limits.
## 2026-06-05 - [Security] Prevent Algorithmic Complexity DoS and numpy crash by validating float parameters
**Vulnerability:** The `run_optimization` function in `src/kimchi_gold/optimal_threshold.py` accepted threshold parameters (min, max, step) as floats but did not validate if they were finite before passing them to `np.arange`. An attacker or programmatic caller supplying `NaN` or `Infinity` could cause a `ValueError` crash (Algorithmic Complexity DoS).
**Learning:** While CLI arguments were validated using `math.isfinite()` in `main()`, the inner API function `run_optimization()` lacked the same validation, leaving programmatic invocations vulnerable to DoS. Additionally, the `backtest.py` file had a missing `import math` which caused a `NameError` crash.
**Prevention:** Always validate all numeric inputs inside core functions using `math.isfinite()` to reject `NaN` and `Inf` values before passing them to math operations or array generators like `np.arange`, ensuring defense in depth regardless of how the function is invoked.

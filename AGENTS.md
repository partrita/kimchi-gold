# AGENTS.md

김치골드 프로젝트 에이전트 가이드: 명명 규칙, 리팩토링 요약, 학습 기록(성능/디자인/보안).

---

## 1. 파일명 및 변수명 가이드

### 개요

김치골드 프로젝트의 파일명과 변수명을 더 명확하고 이해하기 쉽게 개선했습니다. 이 가이드는 새로운 명명 규칙과 구조를 설명합니다.

### 파일명 개선

#### 기존 → 새로운 파일명

| 기존 파일명 | 새로운 파일명 | 역할 설명 |
|------------|-------------|---------|
| `config.py` | `configuration.py` | 프로젝트 설정과 상수 관리 |
| `models.py` | `data_models.py` | 데이터 클래스와 모델 정의 |
| `now_price.py` | `price_fetcher.py` | 가격 데이터 수집 |
| `collect_price.py` | `data_collector.py` | 데이터 수집 및 저장 |
| `kimchi_signal.py` | `outlier_analyzer.py` | 이상치 분석 |
| `plot.py` | `chart_generator.py` | 차트 생성 |

### 함수명 개선

#### 가격 데이터 수집 (price_fetcher.py)

##### 새로운 명확한 함수명:
```python
# 메인 함수
fetch_current_gold_market_data()  # 현재 금 시장 데이터 가져오기

# 개별 데이터 가져오기
fetch_domestic_gold_price()      # 국내 금 가격 가져오기
fetch_international_gold_price()  # 국제 금 가격 가져오기
fetch_usd_krw_exchange_rate()    # USD/KRW 환율 가져오기

# 유틸리티 함수
extract_price_from_naver_finance()                    # 네이버 금융에서 가격 추출
convert_international_gold_price_to_krw_per_gram()    # 국제 금 가격을 원/g으로 환산
calculate_kimchi_premium_values()                     # 김치 프리미엄 계산
```

##### 하위 호환성 별칭:
```python
get_current_gold_price_data = fetch_current_gold_market_data
get_domestic_gold_price = fetch_domestic_gold_price
get_international_gold_price = fetch_international_gold_price
get_usd_krw_rate = fetch_usd_krw_exchange_rate
get_usd_krw = fetch_usd_krw_exchange_rate
```

#### 데이터 수집 및 저장 (data_collector.py)

##### 새로운 명확한 함수명:
```python
# 메인 함수
collect_and_save_current_gold_market_data()  # 현재 금 시장 데이터 수집 및 저장

# 개별 기능
save_gold_price_data_to_csv()        # 금 가격 데이터를 CSV에 저장
check_if_date_already_logged()       # 날짜가 이미 기록되어 있는지 확인
```

##### 하위 호환성 별칭:
```python
collect_current_gold_data = collect_and_save_current_gold_market_data
write_gold_data_to_csv = save_gold_price_data_to_csv
is_today_logged = check_if_date_already_logged
```

#### 이상치 분석 (outlier_analyzer.py)

##### 새로운 명확한 함수명:
```python
# 메인 함수
perform_kimchi_premium_outlier_analysis()  # 김치 프리미엄 이상치 분석 수행

# 개별 기능
determine_if_latest_value_is_outlier()          # 최신값이 이상치인지 판단
calculate_statistical_outlier_boundaries()      # 통계적 이상치 경계값 계산
filter_dataframe_by_recent_dates()             # 최근 날짜로 데이터프레임 필터링
```

##### 하위 호환성 별칭:
```python
analyze_kimchi_premium_outlier = perform_kimchi_premium_outlier_analysis
is_outlier = determine_if_latest_value_is_outlier
calculate_outlier_bounds = calculate_statistical_outlier_boundaries
filter_recent_data = filter_dataframe_by_recent_dates
```

#### 차트 생성 (chart_generator.py)

##### 새로운 명확한 함수명:
```python
# 메인 함수
create_comprehensive_gold_price_charts()  # 종합적인 금 가격 차트 생성

# 개별 차트 생성
generate_kimchi_premium_chart()              # 김치 프리미엄 차트 생성
generate_gold_prices_comparison_chart()      # 금 가격 비교 차트 생성
generate_exchange_rate_trend_chart()         # 환율 트렌드 차트 생성

# 데이터 처리
load_and_preprocess_gold_price_data()       # 금 가격 데이터 로드 및 전처리
```

### 변수명 개선

#### 설정 파일 (configuration.py)

##### 새로운 명확한 변수명:
```python
# 경로 관련
CURRENT_MODULE_DIRECTORY           # 현재 모듈 디렉토리
PROJECT_ROOT_DIRECTORY            # 프로젝트 루트 디렉토리
DATA_STORAGE_DIRECTORY           # 데이터 저장 디렉토리
GOLD_PRICE_DATA_CSV_FILE         # 금 가격 데이터 CSV 파일

# URL 관련
NAVER_DOMESTIC_GOLD_URL          # 네이버 국내 금 가격 URL
NAVER_INTERNATIONAL_GOLD_URL     # 네이버 국제 금 가격 URL
NAVER_USD_KRW_EXCHANGE_URL       # 네이버 USD/KRW 환율 URL

# 기타 설정
REQUEST_HEADERS                  # HTTP 요청 헤더
CSV_COLUMN_HEADERS              # CSV 컬럼 헤더
TROY_OUNCE_TO_GRAM_CONVERSION_RATE  # 트로이 온스에서 그램으로 변환 비율
DEFAULT_CHART_DISPLAY_MONTHS    # 기본 차트 표시 개월 수
CHART_OUTPUT_FILE_NAME          # 차트 출력 파일명
```

#### 데이터 모델 (data_models.py)

##### GoldPriceData 클래스:
```python
@dataclass
class GoldPriceData:
    domestic_price: float                    # 국내 금 가격
    international_price: float               # 국제 금 가격
    usd_krw_rate: float                     # USD/KRW 환율
    international_krw_per_g: float          # 국제 금 가격 (원/g 환산)
    kimchi_premium_amount: float            # 김치 프리미엄 금액
    kimchi_premium_percent: float           # 김치 프리미엄 비율
    data_collection_timestamp: datetime     # 데이터 수집 시간

    # 메서드
    convert_to_csv_row_format()            # CSV 행 형식으로 변환
```

##### ChartGenerationConfiguration 클래스:
```python
@dataclass
class ChartGenerationConfiguration:
    display_months: int                     # 표시할 개월 수
    source_data_filename: str              # 소스 데이터 파일명
    chart_figure_size: tuple              # 차트 피겨 크기
    chart_visual_style: str               # 차트 시각적 스타일

    # 프로퍼티
    generated_output_filename              # 생성된 출력 파일명
```

### 함수 매개변수 개선

#### 가격 수집 함수들:
```python
def extract_price_from_naver_finance(
    target_url: str,                      # 대상 URL
    error_message: str,                   # 오류 메시지
    price_pattern: str = r"[\d,]+(?:\.\d+)?"  # 가격 패턴
) -> float:

def convert_international_gold_price_to_krw_per_gram(
    international_price_usd_per_oz: float,  # 국제 금 가격 (달러/온스)
    usd_krw_exchange_rate: float           # USD/KRW 환율
) -> float:

def calculate_kimchi_premium_values(
    domestic_price_krw_per_gram: float,     # 국내 금 가격 (원/g)
    international_price_krw_per_gram: float # 국제 금 가격 (원/g)
) -> Tuple[float, float]:
```

#### 데이터 수집 함수들:
```python
def check_if_date_already_logged(
    csv_file_path: Path = GOLD_PRICE_DATA_CSV_FILE,
    target_date_to_check: Optional[datetime] = None
) -> bool:

def save_gold_price_data_to_csv(
    gold_price_data_object: GoldPriceData,
    output_csv_file_path: Path = GOLD_PRICE_DATA_CSV_FILE
) -> None:

def collect_and_save_current_gold_market_data(
    output_csv_file_path: Path = GOLD_PRICE_DATA_CSV_FILE,
    skip_if_data_already_exists: bool = True
) -> bool:
```

#### 이상치 분석 함수들:
```python
def calculate_statistical_outlier_boundaries(
    data_series: pd.Series,
    interquartile_range_multiplier: float = 1.5
) -> tuple[float, float]:

def filter_dataframe_by_recent_dates(
    source_dataframe: pd.DataFrame,
    date_column_name: str,
    days_to_look_back: int = 365
) -> pd.DataFrame:

def determine_if_latest_value_is_outlier(
    input_dataframe: pd.DataFrame,
    target_column_name: str,
    date_column_name: str = '날짜',
    analysis_period_days: int = 365,
    iqr_multiplier_threshold: float = 1.5
) -> bool:

def perform_kimchi_premium_outlier_analysis(
    data_csv_file_path: Path = GOLD_PRICE_DATA_CSV_FILE,
    analysis_column_name: str = '김치프리미엄(%)',
    historical_analysis_days: int = 365,
    statistical_threshold_multiplier: float = 1.5
) -> Optional[bool]:
```

#### 차트 생성 함수들:
```python
def load_and_preprocess_gold_price_data(
    source_csv_file_path: Path,
    analysis_period_months: int
) -> pd.DataFrame:

def generate_kimchi_premium_chart(
    chart_axes: Axes,
    chart_data_df: pd.DataFrame,
    display_period_months: int
) -> None:

def generate_gold_prices_comparison_chart(
    chart_axes: Axes,
    chart_data_df: pd.DataFrame,
    display_period_months: int
) -> None:

def generate_exchange_rate_trend_chart(
    chart_axes: Axes,
    chart_data_df: pd.DataFrame,
    display_period_months: int
) -> None:
```

### 사용법 비교

#### 새로운 명확한 방식 (권장):
```python
from kimchi_gold import (
    fetch_current_gold_market_data,
    collect_and_save_current_gold_market_data,
    perform_kimchi_premium_outlier_analysis,
    create_comprehensive_gold_price_charts
)

# 현재 금 시장 데이터 가져오기
current_gold_data = fetch_current_gold_market_data()
print(f"김치 프리미엄: {current_gold_data.kimchi_premium_percent:.2f}%")

# 데이터 수집 및 저장
collection_success = collect_and_save_current_gold_market_data()

# 이상치 분석
outlier_detected = perform_kimchi_premium_outlier_analysis()

# 차트 생성
create_comprehensive_gold_price_charts()
```

#### 기존 방식 (여전히 작동):
```python
from kimchi_gold import (
    get_current_gold_price_data,
    collect_current_gold_data,
    analyze_kimchi_premium_outlier
)

# 기존 방식도 계속 작동
current_data = get_current_gold_price_data()
collect_success = collect_current_gold_data()
outlier_result = analyze_kimchi_premium_outlier()
```

### 혜택

1. **명확성**: 함수명과 변수명만 봐도 기능을 쉽게 이해할 수 있음
2. **일관성**: 모든 함수명이 일관된 명명 규칙(동사 + 명사 + 상세설명 패턴)을 따름
3. **유지보수성**: 코드를 읽고 이해하기 쉬워짐
4. **확장성**: 새로운 기능 추가 시 명명 패턴을 쉽게 따를 수 있음
5. **하위 호환성**: 기존 코드는 수정 없이 계속 작동하며 점진적으로 마이그레이션 가능

---

## 2. 리팩토링 요약

### 개요
김치골드 프로젝트의 코드를 더 이해하기 쉽고 유지보수하기 쉽게 리팩토링했습니다.

### 주요 개선사항

#### 1. 코드 구조 개선

- **새로 추가된 모듈**:
  - `config.py`: 공통 설정과 상수들을 중앙 집중식으로 관리
  - `models.py`: 데이터 클래스와 모델 정의
- **기존 모듈 개선**:
  - `now_price.py`: 더 명확한 함수 분리, 로깅 추가, 에러 처리 개선
  - `collect_price.py`: 새로운 데이터 클래스 활용, 더 명확한 함수명
  - `kimchi_signal.py`: 함수 분해, 더 명확한 로직 구조
  - `__init__.py`: 새로운 함수들과 클래스들을 포함

#### 2. 데이터 클래스 도입

- `GoldPriceData`: 국내/국제 금 가격, 환율, 김치 프리미엄 금액/비율, 수집 시간 등을 담는 데이터클래스
- `ChartConfig`: 차트 표시 개월 수, 데이터 파일명, 피겨 크기, 스타일 설정

#### 3. 함수 개선

**가격 데이터 수집:**
- `get_current_gold_price_data()` → `GoldPriceData` 객체 반환
- `get_domestic_gold_price()` / `get_international_gold_price()` / `get_usd_krw_rate()`

**데이터 저장:**
- `collect_current_gold_data()` / `write_gold_data_to_csv()` / `is_today_logged()`

**분석:**
- `analyze_kimchi_premium_outlier()` / `is_outlier()` / `calculate_outlier_bounds()` / `filter_recent_data()`

#### 4. 에러 처리 및 로깅 개선

- 모든 모듈에 적절한 로깅 추가
- `try-catch` 블록으로 구체적인 예외 처리
- 더 명확한 에러 메시지
- 타임아웃 설정 (HTTP 요청시 10초)

#### 5. 타입 힌트 강화

- 모든 함수에 명확한 타입 힌트 추가
- 반환 타입 명시
- Optional 타입 활용으로 None 가능성 표시

#### 6. 하위 호환성 유지

기존 코드가 계속 작동하도록 레거시 함수들을 유지:
- `calc_kimchi_premium()` → `get_current_gold_price_data()` 호출
- `collect_data()` → `collect_current_gold_data()` 호출
- `check_kimchi_premium_outlier()` → `analyze_kimchi_premium_outlier()` 호출
- `get_usd_krw()` → `get_usd_krw_rate()` 별칭

### 마이그레이션 가이드

1. **즉시 사용 가능**: 기존 코드는 수정 없이 계속 작동
2. **점진적 마이그레이션**: 새로운 함수들을 하나씩 도입
3. **최종 마이그레이션**: 모든 레거시 함수를 새로운 함수로 교체

---

## 3. 학습 기록 — 성능 (bolt)

### 2025-05-14 - Parallelize Market Data Fetching
**Learning:** Using `requests.Session` and `concurrent.futures.ThreadPoolExecutor` to parallelize multiple independent HTTP GET requests can significantly reduce total latency, especially when dealing with multiple external API/web calls. In this case, it reduced fetch time by ~70% (from 2.15s to 0.64s).
**Action:** Always consider parallelizing independent network requests when multiple data points are needed for a single operation. Use a session to reuse connections.

### 2025-05-15 - Optimize Pandas Loop with NumPy
**Learning:** Row-by-row iteration through a Pandas DataFrame using `.loc` is extremely slow due to indexing overhead. For stateful calculations like backtesting, where full vectorization is not possible, converting necessary columns to NumPy arrays (`.values`) before the loop can yield orders-of-magnitude speedups (~160x in this case).
**Action:** Always extract DataFrame columns into NumPy arrays before entering a performance-critical loop that iterates through rows.

---

## 4. 학습 기록 — 디자인 (palette)

### 2025-03-08 - Enhancing Quarto Dashboards with Summary Cards
**Learning:** For static/semi-static dashboards (like Quarto), adding a high-level summary section with visual cards and color indicators significantly improves immediate comprehension of key metrics compared to jumping straight into time-series charts or tables.
**Action:** Always include a summary card section at the top of data dashboards to surface the most critical "right now" information and its state (e.g., positive/negative trends).

---

## 5. 학습 기록 — 보안 (sentinel)

### [Vulnerability] SSRF via Port Manipulation
Validating the URL scheme (`https`) and domain is insufficient defense-in-depth, as attackers can specify arbitrary ports to scan or interact with internal infrastructure.
**Prevention:** Explicitly validate `parsed_url.port` and only permit standard web ports (e.g. `443` or `None` which implies the default for the scheme) during data fetching operations.

### [Vulnerability] Connection Pool Exhaustion DoS
**Vulnerability:** `requests.get` with `stream=True` was used without a `with` context manager. When a `ValueError` was raised for exceeding the size limit (5MB), the underlying connection was not guaranteed to be released back to the pool, leading to resource exhaustion (DoS) when many requests hit the limit.
**Learning:** Reading chunked responses using `iter_content` leaves the connection open if not fully consumed. Raising exceptions before the end of the stream without explicitly closing the response leaks connections.
**Prevention:** Always wrap `requests.get(..., stream=True)` in a `with` context manager to ensure the connection is closed and released, even if an exception is raised early.

### Content-Type validation and Timeout for Slow-Read DoS in streams
**Vulnerability:** Unintended payload processing and Slowloris-style slow-read DoS.
**Learning:** `requests.get` with `stream=True` and a max size check is vulnerable to slow-read attacks where an attacker sends data extremely slowly, exhausting server resources/connection pools, and missing `Content-Type` validation could lead to parsing non-HTML binary payloads using BeautifulSoup.
**Prevention:** To prevent unintended payload types and mitigate Slowloris-style slow-read DoS attacks, explicitly validate the `Content-Type` header (e.g., `text/html`) before reading HTTP responses and enforce a strict absolute time limit within the `requests` streaming loop.

### Input Validation and Length Limits for Price Data
**Vulnerability:** Extracted price data strings were cast to `float` without string length limits, and numerical validation did not account for `NaN`, `Inf`, or unfeasibly large values, posing algorithmic complexity DoS risks (e.g., extremely long float parsing) and data poisoning/logic errors downstream.
**Learning:** External inputs parsed from HTML, even those matched by a regex, must be strictly bounded in both string length before parsing and numerical range after parsing. Missing NaN/Inf checks on floats can lead to unexpected behavior in financial logic.
**Prevention:** Implement strict length limits (e.g., 50 characters) on extracted strings before type conversion to prevent long-string processing overhead. Enhance numeric validation to explicitly reject `math.isnan`, `math.isinf`, and logically excessive values (e.g., > 1,000,000,000) to ensure data integrity and prevent downstream errors.

### Fail-fast Content-Length Validation and Thread Timeouts
**Vulnerability:** A missing fail-fast `Content-Length` check meant the application would start processing chunks of an excessively large payload before aborting, slightly increasing overhead. Concurrently, missing timeouts on `future.result()` calls for threaded network requests could lead to infinite blocking if a request stalled.
**Learning:** Checking payload size only during stream iteration allows attackers to initiate malicious processing, consuming partial resources. Additionally, threads handling network I/O must always have hard timeouts on their results to prevent process hanging.
**Prevention:** Implement a fail-fast mechanism by checking the `Content-Length` HTTP header before stream processing begins, and always enforce explicit timeouts on `.result()` when fetching data via `ThreadPoolExecutor`.

### Robust Fail-fast Content-Length Validation
**Vulnerability:** A logic error in the fail-fast `Content-Length` validation incorrectly caught parsing exceptions (`ValueError`) and unconditionally raised a new `ValueError`, turning malformed headers into a self-inflicted DoS vulnerability instead of falling back to the secondary stream size check.
**Learning:** Exception handling for malformed input during security validation must be carefully isolated so it doesn't inadvertently trigger the security violation handler and cause a DoS.
**Prevention:** When parsing inputs for fail-fast limits, catch parsing errors cleanly and default to safe fallback values (e.g., `None`), allowing secondary defense-in-depth mechanisms to handle the validation.

### SSRF Bypass via Parsing Discrepancies and Homograph Attacks
**Vulnerability:** URL validation only checked if the hostname `endswith(".naver.com")`, but did not strictly validate the characters composing the hostname itself. This lack of character validation opened the door to advanced SSRF bypasses such as IDNA homograph attacks (e.g., using `naver。com` where `。` normalizes to `.`), zero bytes, newline injections, or other parsing discrepancies between `urlparse` and the underlying HTTP client.
**Learning:** Only validating the suffix of a hostname is insufficient against advanced bypass techniques. Different libraries may normalize or parse unusual characters in hostnames differently, leading to cases where a validation check passes but the actual request is routed to an attacker-controlled or unintended destination.
**Prevention:** In addition to validating the domain suffix, enforce a strict allowlist of permitted characters for the `hostname` (e.g., `^[a-zA-Z0-9.-]+$`) using regex before performing further validation. This prevents malicious characters from exploiting parsing discrepancies.

### Prevent Algorithmic Complexity DoS in Number Sequences
**Vulnerability:** Numerical thresholds such as step sizes and bounds (`threshold_step`) in loops or generator functions like `numpy.arange` were passed directly without being validated, making them vulnerable to `ZeroDivisionError` (if step=0) or an Algorithmic Complexity DoS condition by creating immense iterations (if step is an extremely small fraction).
**Learning:** Functions orchestrating loops, ranges, and array generation should not blindly trust input variables passed to them without validation, especially if those variables could be user-controlled CLI parameters.
**Prevention:** Strictly enforce mathematical bounds (`> 0`) on parameter types like step increments and array dimensions, immediately rejecting negative or zero values.

### Missing CLI Parameter Validation
**Vulnerability:** Unbounded CLI parameters and potential for ZeroDivisionError in `optimal_threshold.py` and `backtest.py` via an initial investment <= 0 or extreme float ranges.
**Learning:** External parameters, like CLI arguments, can be crafted to consume excessive memory or divide-by-zero, leading to application crashes.
**Prevention:** Implement strict boundary checks on numeric inputs to prevent both memory exhaustion via unbounded arrays and fatal errors like ZeroDivisionError.

### Enforce Strict Connection Timeouts
**Vulnerability:** External data fetching used a single integer timeout (`timeout=10`) in `requests.get()`. This single value applies to both the connection phase and the read phase. A malicious or uncooperative server could act as a tarpit, accepting the TCP connection but never responding, tying up client resources for the full duration or longer if not carefully managed.
**Learning:** Using a single timeout value in `requests` can lead to resource exhaustion if many connections hang during the initial handshake. Best practice dictates separating connection and read timeouts.
**Prevention:** Always use a tuple for the `timeout` parameter (e.g., `timeout=(3.0, 10.0)`) to ensure the application fails fast if a connection cannot be quickly established, thereby preventing Denial of Service (DoS) via resource exhaustion.

### Enforce math.isfinite on Float CLI Parameters
**Vulnerability:** Float CLI parameters (e.g., `min_threshold`, `max_threshold`, `buy_threshold`, `sell_threshold`) lacked `math.isfinite` validation. When passed non-finite values like `NaN` or `Inf`, the logic downstream produced erratic outcomes or application crashes (such as `ValueError: arange: cannot compute length` during sequence generation in `numpy`).
**Learning:** Python's `float` type natively accepts `NaN` and `Inf`. When these values bypass initial validation and propagate to mathematical operations or sequence generators (like `numpy.arange`), they can lead to unhandled exceptions, logic errors, or DoS conditions.
**Prevention:** Always validate user-provided float inputs using `math.isfinite()` to ensure they are concrete numeric values before executing dependent operations.

### Implement Automated Security Scanning in CI/CD
**Vulnerability:** The application lacked automated security scanning in its CI/CD pipeline. This meant that new vulnerabilities (e.g., insecure coding practices or vulnerable dependencies) could easily be introduced into the `main` branch without detection, increasing the risk of deployment.
**Learning:** Security must be integrated directly into the development workflow as a defense-in-depth measure. Relying solely on manual reviews or ad-hoc scans is insufficient for maintaining a strong security posture. Continuous security scanning ensures that every change is automatically evaluated against known vulnerability databases and secure coding standards.
**Prevention:** Implement a GitHub Actions workflow with restricted permissions (`contents: read`) that automatically runs tools like `bandit` for Static Application Security Testing (SAST) and `pip-audit` for dependency vulnerability scanning on every pull request and push to the main branch.

### Prevent Algorithmic Complexity DoS during Content-Length Parsing
**Vulnerability:** The application parsed the `Content-Length` HTTP header using Python's built-in `int()` function without placing any upper bound on the length of the string to parse.
**Learning:** Calling `int()` on extremely long strings in Python can cause the interpreter to consume significant CPU and memory resources, leading to an Algorithmic Complexity Denial-of-Service (DoS) condition.
**Prevention:** To prevent Algorithmic Complexity DoS from Python's `int()` parsing, enforce strict string length bounds (e.g., `<= 20` characters) before converting HTTP headers like `Content-Length` to integers. Negative sizes should also be rejected to prevent downstream bypasses.

### Prevent Algorithmic Complexity DoS during Date Parsing
**Vulnerability:** The application parsed the `start-date` CLI parameter using `datetime.strptime()` without placing any upper bound on the length of the string to parse.
**Learning:** Calling `datetime.strptime()` on extremely long strings in Python can cause the interpreter to consume significant CPU and memory resources, leading to an Algorithmic Complexity Denial-of-Service (DoS) condition.
**Prevention:** To prevent Algorithmic Complexity DoS from Python's string parsing in `datetime`, enforce strict string length bounds (e.g., `<= 20` characters) before converting parameters like `start-date` to datetime objects.

### Add Audit Logging for Security Events
**Vulnerability:** The codebase implemented robust defenses against SSRF and DoS (validating URL schemes, preventing redirects, checking Content-Length and Content-Type) by silently raising ValueErrors. However, these mitigations lacked an audit trail, meaning that while attacks were stopped, they were not logged or flagged, preventing administrators from observing or reacting to active attacks or misconfigurations.
**Learning:** A security mitigation that simply blocks an action without logging it is incomplete. "Silent" mitigations obscure attack patterns and hinder incident response, as there is no record of the thwarted attempt or its context.
**Prevention:** Whenever a security control blocks an action or input (e.g., rejecting an SSRF attempt or stopping a DoS payload), explicitly log the event (e.g., using `logger.warning("[SECURITY] ...")`) before raising an exception or returning an error. This ensures security event observability.

### Prevent Information Leakage in Error Responses
**Vulnerability:** Raw exception messages (e.g., `collection_error`, `file_write_error`) were appended to user-facing `ValueError`, `IOError`, and `print()` statements in `price_fetcher.py` and `data_collector.py`.
**Learning:** Exposing raw exceptions can inadvertently leak sensitive system information, such as file paths, internal logic states, or network configurations, aiding attackers in reconnaissance.
**Prevention:** To prevent information leakage, securely log the raw exception details internally using a logging framework (`logger.error`), but raise or return generic, user-safe error messages (e.g., "시스템 로그를 확인해주세요.") to the end user.

### Explicitly Enforce TLS Verification
**Vulnerability:** MitM vulnerability via disabled TLS verification
**Learning:** Relying on default library parameters for critical security mechanisms leaves the application vulnerable if defaults are overridden (e.g., globally via env vars) or accidentally changed.
**Prevention:** Explicitly specify security-critical parameters like `verify=True` in `requests` calls to ensure secure defaults are enforced.

### Prevent Information Leakage in CLI Tools
**Vulnerability:** The CLI tools (`backtest.py`, `optimal_threshold.py`, `chart_generator.py`) printed raw exception details and absolute internal server paths (e.g., `Path.cwd()`) directly to standard output upon failure.
**Learning:** Directly printing unhandled exceptions or internal system states to the console in CLI tools or scripts exposes sensitive implementation details (CWE-209), which could be useful to an attacker if the CLI tool's output is inadvertently logged or returned to an unauthorized user in an automated environment (like CI/CD or a wrapper API).
**Prevention:** In CLI scripts, route detailed errors and context (such as file paths and exception stacks) to the internal logging framework using `logger.exception()` or `logger.error()`, and output only generic, safe error messages (e.g., "Error: 시스템 로그를 확인해주세요.") to the user-facing console.

### Secure CI/CD Dependency Installation
**Vulnerability:** The `.github/workflows/publish-website.yml` workflow installed Python dependencies (`pandas`, `plotly`, `jupyter`, `pyyaml`) dynamically via `pip install` without version pinning or vulnerability scanning, making the workflow susceptible to supply chain attacks (e.g., dependency confusion or malicious updates).
**Learning:** Dependencies installed on the fly in CI/CD pipelines without being tracked in the main dependency manifest (`pyproject.toml`) bypass automated security checks (like `pip-audit`) and lack reproducibility.
**Prevention:** To prevent supply chain attacks in CI/CD, all dependencies (including those used for auxiliary tasks like building documentation or websites) must be explicitly declared in the project's dependency manifest (e.g., as an optional dependency group). Update CI scripts to install from this defined group (e.g., `pip install .[website]`) and ensure security scanners (e.g., `pip-audit`) are configured to scan all extras (`--all-extras`).

### Prevent Information Leakage in CLI Tools (Output Paths)
**Vulnerability:** The chart generator CLI script and library printed the absolute internal file paths of the generated charts directly to standard output upon success.
**Learning:** Directly printing absolute file paths to the console in CLI tools or scripts exposes internal system details (CWE-209), which could be useful to an attacker for reconnaissance.
**Prevention:** Output only generic or relative filenames (e.g. `kimchi_gold_price_recent_12months.png`) to the user-facing console, while routing detailed internal context (like absolute file paths) to the logging framework using `logger.info()` for auditing purposes.

### Add Workflow Timeouts
**Vulnerability:** Missing timeout configurations in GitHub Actions workflows.
**Learning:** Without explicit timeouts, compromised dependencies or malicious PRs can intentionally hang CI runners (e.g., infinite loops or cryptomining tarpits), exhausting the repository's GitHub Actions compute quota and causing a Denial of Service (DoS) for the CI/CD pipeline.
**Prevention:** Always define a job-level `timeout-minutes` configuration (e.g., `timeout-minutes: 10`) in all GitHub Actions workflows to enforce strict execution time limits.

### Prevent Information Leakage in Logs
**Vulnerability:** The application used `logger.exception()` extensively across scripts and core modules (`price_fetcher.py`, `backtest.py`, `outlier_analyzer.py`, etc.). `logger.exception()` automatically appends the full stack trace to the log message. Since the application runs in a CI/CD environment (e.g., GitHub Actions), this behavior can inadvertently expose sensitive internal paths, file structures, and library versions into publicly accessible logs, leading to an Information Leakage vulnerability (CWE-209).
**Learning:** Exposing stack traces in production or CI/CD logs provides attackers with valuable reconnaissance information. Internal implementation details should be kept secure. While detailed error information is useful for local debugging, it should be sanitized in centralized or CI/CD logs unless tightly controlled.
**Prevention:** Replace `logger.exception()` with `logger.error()` to log the exception message and relevant contextual data without automatically appending the full stack trace.

### Prevent Algorithmic Complexity DoS and numpy crash by validating float parameters
**Vulnerability:** The `run_optimization` function in `src/kimchi_gold/optimal_threshold.py` accepted threshold parameters (min, max, step) as floats but did not validate if they were finite before passing them to `np.arange`. An attacker or programmatic caller supplying `NaN` or `Infinity` could cause a `ValueError` crash (Algorithmic Complexity DoS).
**Learning:** While CLI arguments were validated using `math.isfinite()` in `main()`, the inner API function `run_optimization()` lacked the same validation, leaving programmatic invocations vulnerable to DoS. Additionally, the `backtest.py` file had a missing `import math` which caused a `NameError` crash.
**Prevention:** Always validate all numeric inputs inside core functions using `math.isfinite()` to reject `NaN` and `Inf` values before passing them to math operations or array generators like `np.arange`, ensuring defense in depth regardless of how the function is invoked.

### Path Traversal Prevention in Data Collectors
**Vulnerability:** The data collection scripts (`src/kimchi_gold/data_collector.py`) directly used a generic Path parameter (`csv_file_path: Path`) to read and write CSV files without validating if the resolved path was within the expected, safe data directory. This could potentially allow Path Traversal attacks (e.g. `Path("../../../../etc/passwd")`) if the input is ever user-supplied.
**Learning:** File path parameters in generic file-writing and reading functions must always be validated against an expected root directory boundary (Defense in Depth), even if the caller currently uses hardcoded constants. Python's `pathlib.Path.resolve().relative_to(base_dir.resolve())` can be used to securely determine if a path remains within a safe boundary.
**Prevention:** Implement a `validate_safe_path` function that resolves the incoming path and uses `relative_to` to check it against the base directory. Call this validation function immediately before executing any file `open()` or `exists()` operations.

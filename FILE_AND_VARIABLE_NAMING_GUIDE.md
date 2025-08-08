# 김치골드 프로젝트 - 명확한 파일명과 변수명 가이드

## 개요

김치골드 프로젝트의 파일명과 변수명을 더 명확하고 이해하기 쉽게 개선했습니다. 이 가이드는 새로운 명명 규칙과 구조를 설명합니다.

## 파일명 개선

### 기존 → 새로운 파일명

| 기존 파일명 | 새로운 파일명 | 역할 설명 |
|------------|-------------|---------|
| `config.py` | `configuration.py` | 프로젝트 설정과 상수 관리 |
| `models.py` | `data_models.py` | 데이터 클래스와 모델 정의 |
| `now_price.py` | `price_fetcher.py` | 가격 데이터 수집 |
| `collect_price.py` | `data_collector.py` | 데이터 수집 및 저장 |
| `kimchi_signal.py` | `outlier_analyzer.py` | 이상치 분석 |
| `plot.py` | `chart_generator.py` | 차트 생성 |

## 함수명 개선

### 가격 데이터 수집 (price_fetcher.py)

#### 새로운 명확한 함수명:
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

#### 하위 호환성 별칭:
```python
get_current_gold_price_data = fetch_current_gold_market_data
get_domestic_gold_price = fetch_domestic_gold_price
get_international_gold_price = fetch_international_gold_price
get_usd_krw_rate = fetch_usd_krw_exchange_rate
get_usd_krw = fetch_usd_krw_exchange_rate
```

### 데이터 수집 및 저장 (data_collector.py)

#### 새로운 명확한 함수명:
```python
# 메인 함수
collect_and_save_current_gold_market_data()  # 현재 금 시장 데이터 수집 및 저장

# 개별 기능
save_gold_price_data_to_csv()        # 금 가격 데이터를 CSV에 저장
check_if_date_already_logged()       # 날짜가 이미 기록되어 있는지 확인
```

#### 하위 호환성 별칭:
```python
collect_current_gold_data = collect_and_save_current_gold_market_data
write_gold_data_to_csv = save_gold_price_data_to_csv
is_today_logged = check_if_date_already_logged
```

### 이상치 분석 (outlier_analyzer.py)

#### 새로운 명확한 함수명:
```python
# 메인 함수
perform_kimchi_premium_outlier_analysis()  # 김치 프리미엄 이상치 분석 수행

# 개별 기능
determine_if_latest_value_is_outlier()          # 최신값이 이상치인지 판단
calculate_statistical_outlier_boundaries()      # 통계적 이상치 경계값 계산
filter_dataframe_by_recent_dates()             # 최근 날짜로 데이터프레임 필터링
```

#### 하위 호환성 별칭:
```python
analyze_kimchi_premium_outlier = perform_kimchi_premium_outlier_analysis
is_outlier = determine_if_latest_value_is_outlier
calculate_outlier_bounds = calculate_statistical_outlier_boundaries
filter_recent_data = filter_dataframe_by_recent_dates
```

### 차트 생성 (chart_generator.py)

#### 새로운 명확한 함수명:
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

## 변수명 개선

### 설정 파일 (configuration.py)

#### 새로운 명확한 변수명:
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

### 데이터 모델 (data_models.py)

#### GoldPriceData 클래스:
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

#### ChartGenerationConfiguration 클래스:
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

## 함수 매개변수 개선

### 가격 수집 함수들:
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

### 데이터 수집 함수들:
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

### 이상치 분석 함수들:
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

### 차트 생성 함수들:
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

## 사용법 비교

### 새로운 명확한 방식 (권장):
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

### 기존 방식 (여전히 작동):
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

## 혜택

### 1. **명확성**
- 함수명과 변수명만 봐도 기능을 쉽게 이해할 수 있음
- `fetch_current_gold_market_data()` vs `calc_kimchi_premium()`
- `collect_and_save_current_gold_market_data()` vs `collect_data()`

### 2. **일관성**
- 모든 함수명이 일관된 명명 규칙을 따름
- 동사 + 명사 + 상세설명 패턴 사용

### 3. **유지보수성**
- 코드를 읽고 이해하기 쉬워짐
- 새로운 개발자들이 빠르게 프로젝트를 이해할 수 있음

### 4. **확장성**
- 새로운 기능 추가 시 명명 패턴을 쉽게 따를 수 있음
- 모듈화된 구조로 기능별 확장이 용이

### 5. **하위 호환성**
- 기존 코드는 수정 없이 계속 작동
- 점진적으로 새로운 명명 방식으로 마이그레이션 가능

## 마이그레이션 전략

1. **즉시 사용**: 새로운 함수명들을 바로 사용할 수 있음
2. **점진적 교체**: 기존 코드를 하나씩 새로운 방식으로 업데이트
3. **완전 마이그레이션**: 모든 레거시 함수를 새로운 함수로 교체

이러한 개선을 통해 김치골드 프로젝트는 더욱 전문적이고 읽기 쉬운 코드베이스가 되었습니다.

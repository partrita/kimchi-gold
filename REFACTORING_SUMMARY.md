# 김치골드 프로젝트 리팩토링 요약

## 개요
김치골드 프로젝트의 코드를 더 이해하기 쉽고 유지보수하기 쉽게 리팩토링했습니다. 주요 개선사항은 다음과 같습니다:

## 주요 개선사항

### 1. 코드 구조 개선

#### 새로 추가된 모듈:
- **`config.py`**: 공통 설정과 상수들을 중앙 집중식으로 관리
- **`models.py`**: 데이터 클래스와 모델 정의

#### 기존 모듈 개선:
- **`now_price.py`**: 더 명확한 함수 분리, 로깅 추가, 에러 처리 개선
- **`collect_price.py`**: 새로운 데이터 클래스 활용, 더 명확한 함수명
- **`kimchi_signal.py`**: 함수 분해, 더 명확한 로직 구조
- **`__init__.py`**: 새로운 함수들과 클래스들을 포함

### 2. 데이터 클래스 도입

#### `GoldPriceData` 클래스:
```python
@dataclass
class GoldPriceData:
    domestic_price: float           # 국내 금 가격 (원/g)
    international_price: float      # 국제 금 가격 (달러/온스)
    usd_krw_rate: float            # 환율 (원/달러)
    international_krw_per_g: float  # 국제 금 가격을 원/g으로 환산
    kimchi_premium_amount: float    # 김치 프리미엄 금액 (원/g)
    kimchi_premium_percent: float   # 김치 프리미엄 비율 (%)
    timestamp: datetime = None      # 데이터 수집 시간
```

#### `ChartConfig` 클래스:
```python
@dataclass
class ChartConfig:
    months: int = 12
    data_filename: str = "kimchi_gold_price_log.csv"
    figsize: tuple = (12, 15)
    style: str = "seaborn-v0_8-whitegrid"
```

### 3. 함수 개선

#### 새로운 메인 함수들:

**가격 데이터 수집:**
- `get_current_gold_price_data()` → `GoldPriceData` 객체 반환
- `get_domestic_gold_price()` → 국내 금 가격
- `get_international_gold_price()` → 국제 금 가격  
- `get_usd_krw_rate()` → USD/KRW 환율

**데이터 저장:**
- `collect_current_gold_data()` → 현재 데이터 수집 및 저장
- `write_gold_data_to_csv()` → 데이터 클래스를 CSV에 저장
- `is_today_logged()` → 오늘 날짜 데이터 존재 여부 확인

**분석:**
- `analyze_kimchi_premium_outlier()` → 김치 프리미엄 이상치 분석
- `is_outlier()` → 일반적인 이상치 검출
- `calculate_outlier_bounds()` → 이상치 경계값 계산
- `filter_recent_data()` → 최근 데이터 필터링

### 4. 에러 처리 및 로깅 개선

- 모든 모듈에 적절한 로깅 추가
- `try-catch` 블록으로 구체적인 예외 처리
- 더 명확한 에러 메시지
- 타임아웃 설정 (HTTP 요청시 10초)

### 5. 타입 힌트 강화

- 모든 함수에 명확한 타입 힌트 추가
- 반환 타입 명시
- Optional 타입 활용으로 None 가능성 표시

### 6. 하위 호환성 유지

기존 코드가 계속 작동하도록 레거시 함수들을 유지:
- `calc_kimchi_premium()` → `get_current_gold_price_data()` 호출
- `collect_data()` → `collect_current_gold_data()` 호출  
- `check_kimchi_premium_outlier()` → `analyze_kimchi_premium_outlier()` 호출
- `get_usd_krw()` → `get_usd_krw_rate()` 별칭

## 사용법

### 새로운 방식 (권장):

```python
from kimchi_gold import get_current_gold_price_data, collect_current_gold_data

# 현재 금 가격 데이터 가져오기
gold_data = get_current_gold_price_data()
print(gold_data)  # 친화적인 문자열 출력

# 데이터 수집하기
success = collect_current_gold_data()
if success:
    print("데이터 수집 성공!")

# 김치 프리미엄 이상치 분석
from kimchi_gold import analyze_kimchi_premium_outlier
result = analyze_kimchi_premium_outlier()
if result:
    print("김치 프리미엄이 이상치입니다!")
```

### 기존 방식 (여전히 작동):

```python
from kimchi_gold.now_price import calc_kimchi_premium
from kimchi_gold.collect_price import collect_data

# 기존 방식도 계속 작동
result = calc_kimchi_premium()
collect_data()
```

## 혜택

1. **가독성 향상**: 더 명확한 함수명과 구조
2. **유지보수성 향상**: 모듈화된 코드와 중앙집중식 설정
3. **확장성**: 데이터 클래스를 활용한 구조화된 데이터 관리  
4. **안정성**: 개선된 에러 처리와 로깅
5. **개발자 경험**: 더 나은 타입 힌트와 문서화
6. **하위 호환성**: 기존 코드 수정 없이 사용 가능

## 마이그레이션 가이드

기존 코드를 새로운 방식으로 점진적으로 마이그레이션할 수 있습니다:

1. **즉시 사용 가능**: 기존 코드는 수정 없이 계속 작동
2. **점진적 마이그레이션**: 새로운 함수들을 하나씩 도입
3. **최종 마이그레이션**: 모든 레거시 함수를 새로운 함수로 교체

이 리팩토링으로 김치골드 프로젝트는 더 전문적이고 유지보수하기 쉬운 코드베이스가 되었습니다.

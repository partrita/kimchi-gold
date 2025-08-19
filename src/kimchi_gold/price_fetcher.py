"""
금 가격 데이터를 네이버 금융에서 가져오는 모듈입니다.
"""

import re
import logging
from typing import Tuple
import requests
from bs4 import BeautifulSoup

from .configuration import (
    REQUEST_HEADERS,
    NAVER_DOMESTIC_GOLD_URL,
    NAVER_INTERNATIONAL_GOLD_URL,
    NAVER_USD_KRW_EXCHANGE_URL,
    TROY_OUNCE_TO_GRAM_CONVERSION_RATE,
)
from .data_models import GoldPriceData

# 로깅 설정
logger = logging.getLogger(__name__)


def extract_price_from_naver_finance(
    target_url: str, error_message: str, price_pattern: str = r"[\d,]+(?:\.\d+)?"
) -> float:
    """
    네이버 금융 페이지에서 가격 정보를 추출하는 공통 함수

    Args:
        target_url: 가격 정보를 가져올 네이버 금융 URL
        error_message: 오류 시 표시할 메시지
        price_pattern: 가격 추출을 위한 정규식 패턴

    Returns:
        추출된 가격 (float)

    Raises:
        requests.RequestException: HTTP 요청 실패 시
        ValueError: 가격 정보를 찾을 수 없을 시
    """
    response = requests.get(target_url, headers=REQUEST_HEADERS, timeout=10)
    response.raise_for_status()  # Raise an exception for bad status codes
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find element with class containing "DetailInfo_price"
    price_tag = soup.find("strong", class_=lambda class_name: class_name and "DetailInfo_price" in class_name)
    if price_tag:
        text = price_tag.get_text()
        price_match = re.search(price_pattern, text)
        if price_match:
            return float(price_match.group().replace(",", ""))
    raise ValueError(error_message)


def fetch_domestic_gold_price() -> float:
    """국내 금 가격을 가져옵니다 (원/g)"""
    return extract_price_from_naver_finance(
        NAVER_DOMESTIC_GOLD_URL, "국내 금 가격 정보를 찾을 수 없습니다."
    )


def fetch_international_gold_price() -> float:
    """국제 금 가격을 가져옵니다 (달러/온스)"""
    return extract_price_from_naver_finance(
        NAVER_INTERNATIONAL_GOLD_URL, "국제 금 가격 정보를 찾을 수 없습니다."
    )


def fetch_usd_krw_exchange_rate() -> float:
    """USD/KRW 환율을 가져옵니다"""
    return extract_price_from_naver_finance(
        NAVER_USD_KRW_EXCHANGE_URL, "환율 정보를 찾을 수 없습니다."
    )


def convert_international_gold_price_to_krw_per_gram(
    international_price_usd_per_oz: float, usd_krw_exchange_rate: float
) -> float:
    """
    국제 금 가격을 원/g 단위로 환산합니다.

    Args:
        international_price_usd_per_oz: 국제 금 가격 (달러/온스)
        usd_krw_exchange_rate: USD/KRW 환율

    Returns:
        원/g 단위로 환산된 국제 금 가격
    """
    return (
        international_price_usd_per_oz * usd_krw_exchange_rate
    ) / TROY_OUNCE_TO_GRAM_CONVERSION_RATE


def calculate_kimchi_premium_values(
    domestic_price_krw_per_gram: float, international_price_krw_per_gram: float
) -> Tuple[float, float]:
    """
    김치 프리미엄을 계산합니다.

    Args:
        domestic_price_krw_per_gram: 국내 금 가격 (원/g)
        international_price_krw_per_gram: 국제 금 가격 (원/g)

    Returns:
        (김치 프리미엄 금액, 김치 프리미엄 비율)
    """
    premium_amount_krw = domestic_price_krw_per_gram - international_price_krw_per_gram
    premium_percentage = (premium_amount_krw / international_price_krw_per_gram) * 100
    return premium_amount_krw, premium_percentage


def fetch_current_gold_market_data() -> GoldPriceData:
    """
    현재 금 가격 데이터를 수집하고 김치 프리미엄을 계산합니다.

    Returns:
        GoldPriceData 객체

    Raises:
        ValueError: 데이터 수집 실패 시
    """
    try:
        logger.info("금 가격 데이터 수집 시작")

        # 각 가격 정보 수집
        domestic_gold_price = fetch_domestic_gold_price()
        international_gold_price = fetch_international_gold_price()
        current_usd_krw_rate = fetch_usd_krw_exchange_rate()

        # 국제 금 가격을 원/g으로 환산
        international_gold_price_krw_per_gram = (
            convert_international_gold_price_to_krw_per_gram(
                international_gold_price, current_usd_krw_rate
            )
        )

        # 김치 프리미엄 계산
        premium_amount, premium_percentage = calculate_kimchi_premium_values(
            domestic_gold_price, international_gold_price_krw_per_gram
        )

        # 데이터 객체 생성
        gold_market_data = GoldPriceData(
            domestic_price=domestic_gold_price,
            international_price=international_gold_price,
            usd_krw_rate=current_usd_krw_rate,
            international_krw_per_g=international_gold_price_krw_per_gram,
            kimchi_premium_amount=premium_amount,
            kimchi_premium_percent=premium_percentage,
        )

        logger.info(f"데이터 수집 완료: 김치 프리미엄 {premium_percentage:.2f}%")
        return gold_market_data

    except Exception as collection_error:
        logger.error(f"금 가격 데이터 수집 실패: {collection_error}")
        raise ValueError(f"금 가격 데이터를 가져올 수 없습니다: {collection_error}")


# 하위 호환성을 위한 레거시 함수들
def calc_kimchi_premium() -> Tuple[float, float, float, float, float, float]:
    """
    레거시 호환성을 위한 함수 - 새로운 코드에서는 fetch_current_gold_market_data() 사용 권장
    """
    gold_market_data = fetch_current_gold_market_data()
    return (
        gold_market_data.domestic_price,
        gold_market_data.international_price,
        gold_market_data.international_krw_per_g,
        gold_market_data.usd_krw_rate,
        gold_market_data.kimchi_premium_amount,
        gold_market_data.kimchi_premium_percent,
    )


# 하위 호환성을 위한 별칭들
get_current_gold_price_data = fetch_current_gold_market_data
get_domestic_gold_price = fetch_domestic_gold_price
get_international_gold_price = fetch_international_gold_price
get_usd_krw_rate = fetch_usd_krw_exchange_rate
get_usd_krw = fetch_usd_krw_exchange_rate


def print_formatted_gold_price(data: GoldPriceData):
    """
    GoldPriceData 객체를 받아 보기 좋은 형태로 터미널에 출력합니다.
    """
    print("--- 현재 금 시세 ---")
    print(f"  - 국내 금 시세 (원/g): {data.domestic_price:,.2f} 원")
    print(f"  - 국제 금 시세 ($/oz): {data.international_price:,.2f} $")
    print(f"  - 환율 (USD/KRW): {data.usd_krw_rate:,.2f} 원")
    print("-" * 20)
    print(f"  -> 국제 금 시세 (원/g 환산): {data.international_krw_per_g:,.2f} 원")
    print(
        f"  -> 김치 프리미엄: {data.kimchi_premium_amount:,.2f} 원 ({data.kimchi_premium_percent:.2f}%)"
    )
    print("--------------------")


def main():
    """
    메인 실행 함수 - 현재 금 가격과 김치 프리미엄을 출력합니다.
    """
    try:
        # 로깅 설정 (콘솔 출력용)

        current_gold_data = fetch_current_gold_market_data()
        print_formatted_gold_price(current_gold_data)

    except Exception as main_error:
        print(f"오류 발생: {main_error}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())

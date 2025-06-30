import re
from typing import Tuple
import requests
from bs4 import BeautifulSoup
from kimchi_gold.config import NAVER_FINANCE_URLS, REQUEST_HEADERS

class PriceScrapingError(Exception):
    """가격 스크래핑 중 에러 발생 시 사용하는 커스텀 예외"""
    pass

def get_price_from_naver(url: str, error_msg: str) -> float:
    """
    네이버 금융에서 가격 정보를 추출하는 공통 함수
    """
    try:
        response = requests.get(url, headers=REQUEST_HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        price_tag = soup.find("strong", class_="DetailInfo_price__I_VJn")
        if price_tag:
            text = price_tag.get_text()
            price_match = re.search(r"[\d,]+(?:\.\d+)?", text)
            if price_match:
                return float(price_match.group().replace(",", ""))
        raise PriceScrapingError(error_msg)
    except requests.RequestException as e:
        raise PriceScrapingError(f"{error_msg} - Request failed: {e}") from e


def get_domestic_gold_price() -> float:
    url = NAVER_FINANCE_URLS["domestic_gold"]
    return get_price_from_naver(url, "국내 금 가격 정보를 찾을 수 없습니다.")


def get_international_gold_price() -> float:
    url = NAVER_FINANCE_URLS["international_gold"]
    return get_price_from_naver(url, "국제 금 가격 정보를 찾을 수 없습니다.")


def get_usd_krw() -> float:
    url = NAVER_FINANCE_URLS["usd_krw"]
    return get_price_from_naver(url, "환율 정보를 찾을 수 없습니다.")


def calc_kimchi_premium() -> Tuple[float, float, float, float, float, float]:
    domestic = get_domestic_gold_price()
    international = get_international_gold_price()
    usdkrw = get_usd_krw()
    international_krw_per_g = (international * usdkrw) / 31.1035
    difference = domestic - international_krw_per_g
    premium_percent = (difference / international_krw_per_g) * 100
    return (
        domestic,
        international,
        international_krw_per_g,
        usdkrw,
        difference,
        premium_percent,
    )


if __name__ == "__main__":
    (
        domestic,
        international,
        international_krw_per_g,
        usdkrw,
        difference,
        premium_percent,
    ) = calc_kimchi_premium()
    print(f"국내 금가격         : {domestic:>12,.2f} 원/g")
    print(f"국제 금 1g 원화환산 : {international_krw_per_g:>12,.2f} 원/g")
    print(f"김치프리미엄        : {difference:>12,.2f} 원/g ({premium_percent:+.2f}%)")

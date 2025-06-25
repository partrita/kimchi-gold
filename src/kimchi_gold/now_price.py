"""
Fetches current gold prices and exchange rates to calculate Kimchi premium.

This module scrapes data from Naver Finance mobile website to get:
- Domestic gold price (KRW per gram)
- International gold price (USD per troy ounce)
- USD/KRW exchange rate

It then calculates the Kimchi premium, which is the percentage difference
between the domestic gold price and the international gold price (converted to KRW per gram).
"""
import re
from typing import Dict, Tuple
import requests
from bs4 import BeautifulSoup

HEADERS: Dict[str, str] = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://m.stock.naver.com/",
}
"""Standard headers used for HTTP requests to mimic a browser."""


def get_price_from_naver(
    url: str, error_msg: str, regex: str = r"[\d,]+(?:\.\d+)?"
) -> float:
    """
    Fetches and extracts a numerical price from a Naver Finance mobile page.

    It looks for a specific HTML structure (<strong> tag with class 'DetailInfo_price__I_VJn')
    and uses a regex to parse the number from its text content.

    :param url: The URL of the Naver Finance page to scrape.
    :type url: str
    :param error_msg: Error message to raise if parsing fails.
    :type error_msg: str
    :param regex: Regular expression to extract the price.
                  Defaults to r"[\\d,]+(?:\\.\\d+)?".
    :type regex: str, optional
    :return: The extracted price as a float.
    :rtype: float
    :raises ValueError: If the price tag is not found, or regex does not match,
                        or the HTTP request fails.
    :raises requests.exceptions.RequestException: For issues like network problems,
                                                  invalid URL, etc.
    """
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()  # Raise an exception for bad status codes
    soup = BeautifulSoup(response.content, "html.parser")
    price_tag = soup.find("strong", class_="DetailInfo_price__I_VJn")
    if price_tag:
        text = price_tag.get_text()
        price_match = re.search(regex, text) # Renamed 'price' to 'price_match'
        if price_match:
            return float(price_match.group().replace(",", ""))
    raise ValueError(error_msg)


def get_domestic_gold_price() -> float:
    """
    Fetches the current domestic gold price (KRW/g) from Naver Finance.

    :return: Domestic gold price in KRW per gram.
    :rtype: float
    :raises ValueError: If the price cannot be fetched or parsed.
    """
    url = "https://m.stock.naver.com/marketindex/metals/M04020000"
    return get_price_from_naver(url, "국내 금 가격 정보를 찾을 수 없습니다.")


def get_international_gold_price() -> float:
    """
    Fetches the current international gold price (USD/troy ounce) from Naver Finance.

    :return: International gold price in USD per troy ounce.
    :rtype: float
    :raises ValueError: If the price cannot be fetched or parsed.
    """
    url = "https://m.stock.naver.com/marketindex/metals/GCcv1"
    return get_price_from_naver(url, "국제 금 가격 정보를 찾을 수 없습니다.")


def get_usd_krw() -> float:
    """
    Fetches the current USD/KRW exchange rate from Naver Finance.

    :return: USD to KRW exchange rate.
    :rtype: float
    :raises ValueError: If the exchange rate cannot be fetched or parsed.
    """
    url = "https://m.stock.naver.com/marketindex/exchange/FX_USDKRW"
    return get_price_from_naver(url, "환율 정보를 찾을 수 없습니다.")


def calc_kimchi_premium() -> Tuple[float, float, float, float, float, float]:
    """
    Calculates the Kimchi premium for gold.

    It fetches domestic gold price, international gold price, and USD/KRW exchange rate.
    Converts international gold price from USD/ounce to KRW/gram.
    The Kimchi premium is the percentage difference between the domestic price (KRW/g)
    and the converted international price (KRW/g).

    :return: A tuple containing:
             - domestic_price (float): Domestic gold price (KRW/g).
             - international_price_usd_oz (float): International gold price (USD/ounce).
             - international_price_krw_g (float): Converted international gold price (KRW/g).
             - usd_krw_rate (float): USD/KRW exchange rate.
             - difference_krw_g (float): Price difference (Domestic - International) in KRW/g.
             - premium_percentage (float): Kimchi premium in percentage.
    :rtype: Tuple[float, float, float, float, float, float]
    """
    domestic: float = get_domestic_gold_price()
    international_usd_oz: float = get_international_gold_price() # Renamed for clarity
    usdkrw_rate: float = get_usd_krw() # Renamed for clarity

    # Convert international price from USD/ounce to KRW/gram
    # 1 troy ounce = 31.1035 grams
    international_krw_g: float = (international_usd_oz * usdkrw_rate) / 31.1035

    difference_krw_g: float = domestic - international_krw_g
    premium_percentage: float = (difference_krw_g / international_krw_g) * 100

    return (
        domestic,
        international_usd_oz,
        international_krw_g,
        usdkrw_rate,
        difference_krw_g,
        premium_percentage,
    )


if __name__ == "__main__":
    # Example usage: Fetch current data and print the Kimchi premium.
    try:
        (
            domestic_price,
            _international_price_usd_oz, # Unused in print
            international_price_krw_g,
            _usdkrw_rate, # Unused in print
            difference,
            premium_percent,
        ) = calc_kimchi_premium()

        print(f"국내 금가격         : {domestic_price:>12,.2f} 원/g")
        print(f"국제 금 1g 원화환산 : {international_price_krw_g:>12,.2f} 원/g")
        print(f"김치프리미엄        : {difference:>12,.2f} 원/g ({premium_percent:+.2f}%)")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Naver Finance: {e}")
    except ValueError as e:
        print(f"Error processing price data: {e}")

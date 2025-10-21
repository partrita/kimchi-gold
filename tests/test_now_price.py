import pytest
from unittest.mock import patch
from kimchi_gold import price_fetcher

MOCK_DOMESTIC_PRICE_TEXT = "80,123.45"
MOCK_INTERNATIONAL_PRICE_TEXT = "1,999.99"
MOCK_USD_KRW_TEXT = "1,355.67"


def test_get_price_from_naver_success():
    url = "http://example.com"
    error_msg = "테스트 에러 메시지"

    with (
        patch("requests.get") as mock_get,
        patch("kimchi_gold.price_fetcher.BeautifulSoup") as mock_bs,
    ):
        mock_get.return_value.content = f"""
            <html>
                <body>
                    <strong class="DetailInfo_price__I_VJn">{MOCK_DOMESTIC_PRICE_TEXT}</strong>
                </body>
            </html>
        """.encode("utf-8")
        mock_soup_instance = mock_bs.return_value
        mock_soup_instance.find.return_value.get_text.return_value = (
            MOCK_DOMESTIC_PRICE_TEXT
        )

        price = price_fetcher.extract_price_from_naver_finance(url, error_msg)
        assert price == float(MOCK_DOMESTIC_PRICE_TEXT.replace(",", ""))
        mock_get.assert_called_once_with(
            url, headers=price_fetcher.REQUEST_HEADERS, timeout=10
        )
        mock_bs.assert_called_once_with(mock_get.return_value.content, "html.parser")
        # class_ 파라미터가 람다 함수이므로 호출 여부만 확인
        mock_soup_instance.find.assert_called_once()
        call_args = mock_soup_instance.find.call_args
        assert call_args[0][0] == "strong"  # 첫 번째 인자가 "strong"인지 확인
        assert "class_" in call_args[1]  # class_ 키워드 인자가 있는지 확인


def test_get_price_from_naver_no_price_tag():
    url = "http://example.com"
    error_msg = "테스트 에러 메시지"

    with (
        patch("requests.get") as mock_get,
        patch("kimchi_gold.price_fetcher.BeautifulSoup") as mock_bs,
    ):
        mock_get.return_value.content = """
            <html>
                <body>
                    <div>No price here</div>
                </body>
            </html>
        """.encode("utf-8")
        mock_soup_instance = mock_bs.return_value
        mock_soup_instance.find.return_value = None

        with pytest.raises(ValueError) as excinfo:
            price_fetcher.extract_price_from_naver_finance(url, error_msg)
        assert str(excinfo.value) == error_msg
        mock_get.assert_called_once_with(
            url, headers=price_fetcher.REQUEST_HEADERS, timeout=10
        )
        mock_bs.assert_called_once_with(mock_get.return_value.content, "html.parser")
        # class_ 파라미터가 람다 함수이므로 호출 여부만 확인
        mock_soup_instance.find.assert_called_once()
        call_args = mock_soup_instance.find.call_args
        assert call_args[0][0] == "strong"  # 첫 번째 인자가 "strong"인지 확인
        assert "class_" in call_args[1]  # class_ 키워드 인자가 있는지 확인


def test_get_price_from_naver_no_price_in_text():
    url = "http://example.com"
    error_msg = "테스트 에러 메시지"

    with (
        patch("requests.get") as mock_get,
        patch("kimchi_gold.price_fetcher.BeautifulSoup") as mock_bs,
    ):
        mock_get.return_value.content = """
            <html>
                <body>
                    <strong class="DetailInfo_price__I_VJn">문자열</strong>
                </body>
            </html>
        """.encode("utf-8")
        mock_soup_instance = mock_bs.return_value
        mock_soup_instance.find.return_value.get_text.return_value = "문자열"

        with pytest.raises(ValueError) as excinfo:
            price_fetcher.extract_price_from_naver_finance(url, error_msg)
        assert str(excinfo.value) == error_msg
        mock_get.assert_called_once_with(
            url, headers=price_fetcher.REQUEST_HEADERS, timeout=10
        )
        mock_bs.assert_called_once_with(mock_get.return_value.content, "html.parser")
        # class_ 파라미터가 람다 함수이므로 호출 여부만 확인
        mock_soup_instance.find.assert_called_once()
        call_args = mock_soup_instance.find.call_args
        assert call_args[0][0] == "strong"  # 첫 번째 인자가 "strong"인지 확인
        assert "class_" in call_args[1]  # class_ 키워드 인자가 있는지 확인


@patch("kimchi_gold.price_fetcher.extract_price_from_naver_finance")
def test_get_domestic_gold_price_success(mock_get_price):
    mock_get_price.return_value = float(MOCK_DOMESTIC_PRICE_TEXT.replace(",", ""))
    price = price_fetcher.fetch_domestic_gold_price()
    assert price == float(MOCK_DOMESTIC_PRICE_TEXT.replace(",", ""))
    mock_get_price.assert_called_once()


@patch("kimchi_gold.price_fetcher.extract_price_from_naver_finance")
def test_get_international_gold_price_success(mock_get_price):
    mock_get_price.return_value = float(MOCK_INTERNATIONAL_PRICE_TEXT.replace(",", ""))
    price = price_fetcher.fetch_international_gold_price()
    assert price == float(MOCK_INTERNATIONAL_PRICE_TEXT.replace(",", ""))
    mock_get_price.assert_called_once()


@patch("kimchi_gold.price_fetcher.extract_price_from_naver_finance")
def test_get_usd_krw_success(mock_get_price):
    mock_get_price.return_value = float(MOCK_USD_KRW_TEXT.replace(",", ""))
    price = price_fetcher.fetch_usd_krw_exchange_rate()
    assert price == float(MOCK_USD_KRW_TEXT.replace(",", ""))
    mock_get_price.assert_called_once()

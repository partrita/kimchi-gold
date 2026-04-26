import pytest
from unittest.mock import patch
from kimchi_gold import price_fetcher

MOCK_DOMESTIC_PRICE_TEXT = "80,123.45"
MOCK_INTERNATIONAL_PRICE_TEXT = "1,999.99"
MOCK_USD_KRW_TEXT = "1,355.67"


def test_get_price_from_naver_success():
    url = "https://finance.naver.com"
    error_msg = "테스트 에러 메시지"

    with (
        patch("requests.get") as mock_get,
        patch("kimchi_gold.price_fetcher.BeautifulSoup") as mock_bs,
    ):
        mock_get.return_value.__enter__.return_value.is_redirect = False
        mock_get.return_value.__enter__.return_value.headers = {"Content-Type": "text/html; charset=utf-8"}
        content = f"""
            <html>
                <body>
                    <strong class="DetailInfo_price__I_VJn">{MOCK_DOMESTIC_PRICE_TEXT}</strong>
                </body>
            </html>
        """.encode("utf-8")
        mock_get.return_value.__enter__.return_value.iter_content.return_value = [content]
        mock_soup_instance = mock_bs.return_value
        mock_soup_instance.find.return_value.get_text.return_value = (
            MOCK_DOMESTIC_PRICE_TEXT
        )

        price = price_fetcher.extract_price_from_naver_finance(url, error_msg)
        assert price == float(MOCK_DOMESTIC_PRICE_TEXT.replace(",", ""))
        mock_get.assert_called_once_with(
            url, headers=price_fetcher.REQUEST_HEADERS, timeout=10, allow_redirects=False, stream=True
        )
        mock_bs.assert_called_once_with(content, "html.parser")
        # class_ 파라미터가 람다 함수이므로 호출 여부만 확인
        mock_soup_instance.find.assert_called_once()
        call_args = mock_soup_instance.find.call_args
        assert call_args[0][0] == "strong"  # 첫 번째 인자가 "strong"인지 확인
        assert "class_" in call_args[1]  # class_ 키워드 인자가 있는지 확인


def test_get_price_from_naver_no_price_tag():
    url = "https://finance.naver.com"
    error_msg = "테스트 에러 메시지"

    with (
        patch("requests.get") as mock_get,
        patch("kimchi_gold.price_fetcher.BeautifulSoup") as mock_bs,
    ):
        mock_get.return_value.__enter__.return_value.is_redirect = False
        mock_get.return_value.__enter__.return_value.headers = {"Content-Type": "text/html"}
        content = """
            <html>
                <body>
                    <div>No price here</div>
                </body>
            </html>
        """.encode("utf-8")
        mock_get.return_value.__enter__.return_value.iter_content.return_value = [content]
        mock_soup_instance = mock_bs.return_value
        mock_soup_instance.find.return_value = None

        with pytest.raises(ValueError) as excinfo:
            price_fetcher.extract_price_from_naver_finance(url, error_msg)
        assert str(excinfo.value) == error_msg
        mock_get.assert_called_once_with(
            url, headers=price_fetcher.REQUEST_HEADERS, timeout=10, allow_redirects=False, stream=True
        )
        mock_bs.assert_called_once_with(content, "html.parser")
        # class_ 파라미터가 람다 함수이므로 호출 여부만 확인
        mock_soup_instance.find.assert_called_once()
        call_args = mock_soup_instance.find.call_args
        assert call_args[0][0] == "strong"  # 첫 번째 인자가 "strong"인지 확인
        assert "class_" in call_args[1]  # class_ 키워드 인자가 있는지 확인


def test_get_price_from_naver_no_price_in_text():
    url = "https://finance.naver.com"
    error_msg = "테스트 에러 메시지"

    with (
        patch("requests.get") as mock_get,
        patch("kimchi_gold.price_fetcher.BeautifulSoup") as mock_bs,
    ):
        mock_get.return_value.__enter__.return_value.is_redirect = False
        mock_get.return_value.__enter__.return_value.headers = {"Content-Type": "text/html"}
        content = """
            <html>
                <body>
                    <strong class="DetailInfo_price__I_VJn">문자열</strong>
                </body>
            </html>
        """.encode("utf-8")
        mock_get.return_value.__enter__.return_value.iter_content.return_value = [content]
        mock_soup_instance = mock_bs.return_value
        mock_soup_instance.find.return_value.get_text.return_value = "문자열"

        with pytest.raises(ValueError) as excinfo:
            price_fetcher.extract_price_from_naver_finance(url, error_msg)
        assert str(excinfo.value) == error_msg
        mock_get.assert_called_once_with(
            url, headers=price_fetcher.REQUEST_HEADERS, timeout=10, allow_redirects=False, stream=True
        )
        mock_bs.assert_called_once_with(content, "html.parser")
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


def test_extract_price_invalid_values():
    url = "https://finance.naver.com"
    error_msg = "국내 금 가격 정보를 찾을 수 없습니다."

    with (
        patch("requests.get") as mock_get,
        patch("kimchi_gold.price_fetcher.BeautifulSoup") as mock_bs,
    ):
        mock_get.return_value.__enter__.return_value.is_redirect = False
        mock_get.return_value.__enter__.return_value.headers = {"Content-Type": "text/html"}
        mock_get.return_value.__enter__.return_value.iter_content.return_value = [b"<html><body><strong class='price'>0</strong></body></html>"]
        mock_soup_instance = mock_bs.return_value
        mock_soup_instance.find.return_value.get_text.return_value = "0"

        with pytest.raises(ValueError) as excinfo:
            price_fetcher.extract_price_from_naver_finance(url, error_msg)
        assert "유효하지 않은" in str(excinfo.value)
        assert "0 이하" in str(excinfo.value)


def test_extract_price_ssrf_protection_invalid_scheme():
    url = "ftp://finance.naver.com"
    error_msg = "테스트 에러 메시지"
    with pytest.raises(ValueError) as excinfo:
        price_fetcher.extract_price_from_naver_finance(url, error_msg)
    assert "Invalid URL scheme" in str(excinfo.value)


def test_extract_price_ssrf_protection_http_not_allowed():
    url = "http://finance.naver.com"
    error_msg = "테스트 에러 메시지"
    with pytest.raises(ValueError) as excinfo:
        price_fetcher.extract_price_from_naver_finance(url, error_msg)
    assert "Only HTTPS is allowed for security" in str(excinfo.value)


def test_extract_price_ssrf_protection_invalid_domain():
    url = "https://example.com"
    error_msg = "테스트 에러 메시지"
    with pytest.raises(ValueError) as excinfo:
        price_fetcher.extract_price_from_naver_finance(url, error_msg)
    assert "Invalid domain" in str(excinfo.value)


def test_extract_price_ssrf_protection_no_redirects():
    url = "https://finance.naver.com"
    error_msg = "테스트 에러 메시지"

    with patch("requests.get") as mock_get:
        mock_get.return_value.is_redirect = True
        with pytest.raises(ValueError) as excinfo:
            price_fetcher.extract_price_from_naver_finance(url, error_msg)
        assert "Redirects are not allowed for security reasons" in str(excinfo.value)

def test_extract_price_ssrf_protection_bypass():
    url = "https://127.0.0.1\\@naver.com/"
    error_msg = "테스트 에러 메시지"
    with pytest.raises(ValueError) as excinfo:
        price_fetcher.extract_price_from_naver_finance(url, error_msg)
    assert "URL must not contain userinfo (@)" in str(excinfo.value)


def test_extract_price_ssrf_protection_backslash_bypass():
    url = "https://127.0.0.1\\.naver.com/"
    error_msg = "테스트 에러 메시지"
    with pytest.raises(ValueError) as excinfo:
        price_fetcher.extract_price_from_naver_finance(url, error_msg)
    assert "URL must not contain backslashes" in str(excinfo.value)


def test_extract_price_ssrf_protection_invalid_port():
    url = "https://finance.naver.com:8080/"
    error_msg = "테스트 에러 메시지"
    with pytest.raises(ValueError) as excinfo:
        price_fetcher.extract_price_from_naver_finance(url, error_msg)
    assert "Invalid port" in str(excinfo.value)


def test_extract_price_ssrf_protection_invalid_hostname_characters():
    url = "https://finance.naver。com/"
    error_msg = "테스트 에러 메시지"
    with pytest.raises(ValueError) as excinfo:
        price_fetcher.extract_price_from_naver_finance(url, error_msg)
    assert "Invalid hostname characters" in str(excinfo.value)


def test_extract_price_invalid_content_type():
    url = "https://finance.naver.com"
    error_msg = "테스트 에러 메시지"

    with patch("requests.get") as mock_get:
        mock_get.return_value.__enter__.return_value.is_redirect = False
        mock_get.return_value.__enter__.return_value.headers = {"Content-Type": "application/json"}

        with pytest.raises(ValueError) as excinfo:
            price_fetcher.extract_price_from_naver_finance(url, error_msg)
        assert "Invalid Content-Type" in str(excinfo.value)

def test_extract_price_content_length_exceeds_limit():
    url = "https://finance.naver.com"
    error_msg = "테스트 에러 메시지"

    with patch("requests.get") as mock_get:
        mock_get.return_value.__enter__.return_value.is_redirect = False
        mock_get.return_value.__enter__.return_value.headers = {
            "Content-Type": "text/html",
            "Content-Length": str(6 * 1024 * 1024) # 6MB, exceeds 5MB
        }

        with pytest.raises(ValueError) as excinfo:
            price_fetcher.extract_price_from_naver_finance(url, error_msg)
        assert "Response size exceeds the maximum limit (5MB) based on Content-Length." in str(excinfo.value)

def test_extract_price_slow_read_dos_timeout():
    url = "https://finance.naver.com"
    error_msg = "테스트 에러 메시지"

    with patch("requests.get") as mock_get, patch("kimchi_gold.price_fetcher.time.monotonic") as mock_time:
        mock_get.return_value.__enter__.return_value.is_redirect = False
        mock_get.return_value.__enter__.return_value.headers = {"Content-Type": "text/html"}

        # iter_content yields two chunks
        mock_get.return_value.__enter__.return_value.iter_content.return_value = [b"chunk1", b"chunk2"]

        # Simulate time passing more than 10 seconds between chunks
        mock_time.side_effect = [0, 0, 11] # first call sets start_time, second call in first iteration loop, third call in second iteration loop

        with pytest.raises(ValueError) as excinfo:
            price_fetcher.extract_price_from_naver_finance(url, error_msg)
        assert "Response reading timed out (Slowloris mitigation)." in str(excinfo.value)

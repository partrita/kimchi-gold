# Sentinel Journal

## 2026-03-09 - Price Validation Enhancement
**Vulnerability:** Fetched gold prices from external web sources (Naver Finance) were used directly in calculations without validation. Malformed HTML or temporary zero-price service outages could result in `ZeroDivisionError` (DoS) or corrupted data logs.
**Learning:** External data should never be trusted, even from reliable financial portals. Logic that performs division (like premium percentage) is particularly sensitive to zero values. 
**Prevention:** Implement a `validate_price` layer for all scraped numbers to ensure they are positive floats before they reach the data processing or storage layers.


## 2025-05-14 - [Parallelize Market Data Fetching]
**Learning:** Using `requests.Session` and `concurrent.futures.ThreadPoolExecutor` to parallelize multiple independent HTTP GET requests can significantly reduce total latency, especially when dealing with multiple external API/web calls. In this case, it reduced fetch time by ~70% (from 2.15s to 0.64s).
**Action:** Always consider parallelizing independent network requests when multiple data points are needed for a single operation. Use a session to reuse connections.

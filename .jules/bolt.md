
## 2025-05-14 - [Parallelize Market Data Fetching]
**Learning:** Using `requests.Session` and `concurrent.futures.ThreadPoolExecutor` to parallelize multiple independent HTTP GET requests can significantly reduce total latency, especially when dealing with multiple external API/web calls. In this case, it reduced fetch time by ~70% (from 2.15s to 0.64s).
**Action:** Always consider parallelizing independent network requests when multiple data points are needed for a single operation. Use a session to reuse connections.

## 2025-05-15 - [Optimize Pandas Loop with NumPy]
**Learning:** Row-by-row iteration through a Pandas DataFrame using `.loc` is extremely slow due to indexing overhead. For stateful calculations like backtesting, where full vectorization is not possible, converting necessary columns to NumPy arrays (`.values`) before the loop can yield orders-of-magnitude speedups (~160x in this case).
**Action:** Always extract DataFrame columns into NumPy arrays before entering a performance-critical loop that iterates through rows.

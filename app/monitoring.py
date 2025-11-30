import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from prometheus_client import Counter, Histogram

SERVICE = "meningkitobimbot"

REQUEST_COUNT = Counter(
    "http_requests_total", "HTTP so‘rovlar soni",
    ["service","method","endpoint","status","user"]
)
REQUEST_LATENCY = Histogram(
    "http_request_latency_seconds", "Javob vaqti",
    ["service","endpoint"]
)

BOOKS_SEARCH = Counter(
    "books_search_total", "Kitob qidirishlar",
    ["service","query","user"]
)
RECOMMEND_REQ = Counter(
    "recommend_requests_total", "Recommendation so‘rovlari",
    ["service","user"]
)
RATE_LIMIT_EXCEED = Counter(
    "chat_limit_exceeded_total", "Chat limit oshdi",
    ["service","chat"]
)

class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        user = request.headers.get("X-User", "anon")
        endpoint = request.url.path
        method = request.method
        start = time.perf_counter()
        resp = await call_next(request)
        status = str(resp.status_code)
        REQUEST_COUNT.labels(
            service=SERVICE, method=method, endpoint=endpoint, status=status, user=user
        ).inc()
        REQUEST_LATENCY.labels(service=SERVICE, endpoint=endpoint).observe(time.perf_counter()-start)
        return resp

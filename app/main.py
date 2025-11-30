from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response

# Prometheus metriclari
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint", "http_status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP Request latency",
    ["endpoint"]
)

class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, scope, receive, send):
        if scope["type"] != "http":
            return await super().dispatch(scope, receive, send)

        method = scope["method"]
        endpoint = scope["path"]

        with REQUEST_LATENCY.labels(endpoint).time():
            status_code_container = []

            async def send_wrapper(message):
                if message["type"] == "http.response.start":
                    status = message["status"]
                    status_code_container.append(status)
                await send(message)

            await super().dispatch(scope, receive, send_wrapper)

            status = status_code_container[0] if status_code_container else 500
            REQUEST_COUNT.labels(method, endpoint, str(status)).inc()

app = FastAPI(title="Mening Kitobim Bot")

# Middleware qo‘shish
app.add_middleware(PrometheusMiddleware)

# Test endpoint
@app.get("/")
async def root():
    return {"status": "ok", "service": "meningkitobimbot"}

# Prometheus scrape endpoint
@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")

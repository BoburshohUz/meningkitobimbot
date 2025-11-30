from fastapi import FastAPI, Request, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from starlette.middleware.base import BaseHTTPMiddleware
import logging

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("kitob-bot")

# Prometheus counters
reservations_total = Counter("reservations_total","Jami rezervlar")
qr_scan_total = Counter("qr_scan_total","Jami QR skanlar")

app = FastAPI(title="Mening Kitobim Bot")

# Middleware (to‘g‘ri import!)
class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/webhook" and request.method == "POST":
            qr_scan_total.inc()
        response = await call_next(request)
        return response

# Middleware qo‘shish
app.add_middleware(PrometheusMiddleware)

# Metrics endpoint
@app.get("/metrics")
async def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)

# Telegram webhook endpoint
@app.post("/webhook")
async def webhook(request: Request):
    try:
        body = await request.json()
        logger.info(f"Webhook keldi, size={len(str(body))}")
        reservations_total.inc()
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}

# Root endpoint
@app.get("/")
async def root():
    return {"status": "ok", "service": "kitob-bot alive"}

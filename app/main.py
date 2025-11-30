from fastapi import FastAPI, Request
import logging
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from starlette.middleware.base import BaseHTTPMiddleware

# Log sozlash
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("kitob-bot")

# Monitoring metricalar
reservations_total = Counter("reservations_total", "Jami kitob rezervlari")
qr_scan_total = Counter("qr_scan_total", "QR skanlar soni")

# FastAPI ilovasi
app = FastAPI(title="Mening Kitobim Bot")

# Prometheus middleware
class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if request.method == "POST" and request.url.path == "/webhook":
            qr_scan_total.inc()
        return response

app.add_middleware(PrometheusMiddleware)

# Metrics endpoint
@app.get("/metrics")
async def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)

# Telegram webhook endpoint
@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        body = await request.json()
        logger.info(f"Webhook data keldi, size={len(str(body))}")
        reservations_total.inc()
        return {"ok": True, "message": "Webhook qabul qilindi ✅"}
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return {"ok": False, "error": str(e)}

# Root test
@app.get("/")
async def root():
    return {"status": "ok", "service": "kitob-bot", "message": "Server ishga tushdi ✅"}

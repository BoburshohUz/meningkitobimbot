from fastapi import FastAPI, Request, Response
import logging
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from starlette.middleware.base import BaseHTTPMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("kitob-bot")

reservations_total = Counter("reservations_total", "Jami kitob rezervlari")
qr_scan_total = Counter("qr_scan_total", "QR skanlar soni")

app = FastAPI(title="Mening Kitobim Bot")

class PrometheusMiddleware(BaseHttpMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if request.method == "POST" and request.url.path == "/webhook":
            qr_scan_total.inc()
        return response

app.add_middleware(PrometheusMiddleware)

@app.get("/metrics")
async def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)

@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        body = await request.json()
        logger.info(f"Webhook qabul qilindi, size={len(str(body))}")
        reservations_total.inc()
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}

@app.get("/")
async def root():
    return {"status":"ok"}

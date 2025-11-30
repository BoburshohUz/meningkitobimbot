from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from prometheus_client import Counter, generate_latest
from starlette.middleware.base import BaseHTTPMiddleware

# Monitoring counters
reservations_total = Counter("reservations_total", "Total reservations")
qr_scan_total = Counter("qr_scan_total", "QR scan total")

# FastAPI app
app = FastAPI(title="MeningKitobimBot Minimal")

# CORS (hamma joydan so‘rovga ruxsat)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Prometheus Middleware minimal
class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, scope, receive, send):
        await super().dispatch(scope, receive, send)

app.add_middleware(PrometheusMiddleware)

# Webhook endpoint (POST)
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    
    # Monitoring increment
    qr_scan_total.inc()
    reservations_total.inc()

    return {"ok": True, "received_fields": list(data.keys()), "size": len(str(data))}

# Root (/) – server alive ni ko‘rsatadi
@app.get("/")
async def root():
    return {"status": "ok", "service": "kitob-bot alive"}

# Metrics endpoint
@app.get("/metrics")
async def metrics():
    return generate_latest()

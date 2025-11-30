from prometheus_client import Counter
reservations_total = Counter("reservations_total","Total reservations")
qr_scan_total = Counter("qr_scan_total","QR scan total")

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from .settings import settings
from .middleware.ip_allowlist import IPAllowlistMiddleware
from .logging_config import configure_logging

configure_logging()
app = FastAPI(title="MeningKitobimBot")

# Qo‘shilgan Monitoring + Rate limit + QR
from .monitoring import PrometheusMiddleware, metrics_endpoint
from .middleware.rate_limit import RateLimitMiddleware
from .qr import router as qr_router

app.add_middleware(RateLimitMiddleware)
app.add_middleware(PrometheusMiddleware)
app.include_router(qr_router, prefix="/api")
app.add_route("/metrics", metrics_endpoint)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# IP allowlist
if settings.IP_ALLOWLIST:
    app.add_middleware(IPAllowlistMiddleware)

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    qr_scan_total.inc()
    return {"ok":True, "size": len(str(data))}

@app.get("/")
async def root():
    return {"status":"ok","service":"kitob-bot"}

from .recommend import router as recommend_router
app.include_router(recommend_router, prefix='/api')

# Prometheus metrics mounted at /metrics

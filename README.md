

## Additional components added
- Prometheus metrics (`/metrics`) and middleware
- Redis caching wrapper (`app/cache.py`)
- Rate limit middleware using Redis (`app/middleware/rate_limit.py`)
- QR scanner endpoint (`POST /api/scan_qr`) using Pillow + pyzbar

**Note:** `pyzbar` may require system library `zbar` to be installed in the Docker image or host system. Update Dockerfile accordingly.

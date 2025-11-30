from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
import time,os,aioredis

REDIS_URL=os.getenv("REDIS_URL","redis://localhost:6379/0")
LIMIT_IP=int(os.getenv("RATE_LIMIT_IP","40"))
LIMIT_USER=int(os.getenv("RATE_LIMIT_USER","100"))
WINDOW=60

async def redis():
    return await aioredis.from_url(REDIS_URL,decode_responses=True)

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        r=await redis()
        try:
            ip=request.client.host if request.client else "anon"
            token=request.headers.get("Authorization","").replace("Bearer ","")
            bucket=int(time.time()//WINDOW)
            key_ip=f"rl:ip:{ip}:{bucket}"
            c_ip=await r.incr(key_ip)
            if c_ip==1: await r.expire(key_ip,WINDOW)
            if c_ip>LIMIT_IP: 
                raise HTTPException(429,"IP лимитdan oshdi")
            if token:
                key_u=f"rl:user:{token}:{bucket}"
                c_u=await r.incr(key_u)
                if c_u==1: await r.expire(key_u,WINDOW)
                if c_u>LIMIT_USER:
                    raise HTTPException(429,"User лимитdan oshdi")
        finally:
            await r.close()
        return await call_next(request)

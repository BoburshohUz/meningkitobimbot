import aioredis
import os
import json
from typing import Optional

REDIS_URL = os.getenv('REDIS_URL', os.getenv('REDIS', 'redis://localhost:6379/0'))

async def get_redis():
    return await aioredis.from_url(REDIS_URL, decode_responses=True)

async def cache_get(key: str) -> Optional[dict]:
    r = await get_redis()
    data = await r.get(key)
    if not data:
        return None
    try:
        return json.loads(data)
    finally:
        await r.close()

async def cache_set(key: str, value: dict, expire: int = 60):
    r = await get_redis()
    await r.set(key, json.dumps(value), ex=expire)
    await r.close()

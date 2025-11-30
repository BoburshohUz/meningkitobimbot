from pydantic import BaseSettings, AnyUrl
from typing import List, Optional

class Settings(BaseSettings):
    BOT_TOKEN: str
    WEBHOOK_URL: str
    DATABASE_URL: str
    STORJ_BASE_URL: Optional[str] = None
    ADMIN_IDS: str = ""
    PORT: int = 8000
    ES_URL: Optional[str] = None
    REDIS_URL: Optional[str] = None
    IP_ALLOWLIST: Optional[str] = ""

    @property
    def admin_list(self) -> List[int]:
        if not self.ADMIN_IDS:
            return []
        return [int(x.strip()) for x in self.ADMIN_IDS.split(",") if x.strip().isdigit()]

    class Config:
        env_file = ".env"

settings = Settings()

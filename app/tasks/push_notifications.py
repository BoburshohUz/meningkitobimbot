from celery import Celery
import os

BROKER=os.getenv("REDIS_URL","redis://localhost:6379/0")
celery_app = Celery("push", broker=BROKER, backend=BROKER)

@celery_app.task
def broadcast(msg: str, chat_id: int):
    import requests
    bot = os.getenv("BOT_TOKEN")
    requests.post(f"https://api.telegram.org/bot{bot}/sendMessage",
                  json={"chat_id":chat_id,"text":msg}, timeout=10)

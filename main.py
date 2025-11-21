from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    chat_id = data.get("message", {}).get("chat", {}).get("id")
    text = data.get("message", {}).get("text")

    if chat_id and text:
        async with httpx.AsyncClient() as client:
            await client.post(f"{API_URL}/sendMessage", json={
                "chat_id": chat_id,
                "text": "Bot ishlayapti! Siz yozdingiz: " + text
            })

    return {"ok": True}

@app.get("/")
def home():
    return {"status": "running"}

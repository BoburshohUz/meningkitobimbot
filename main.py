import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.getenv("BOT_TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}/"


def send_message(chat_id, text):
    requests.post(URL + "sendMessage", json={"chat_id": chat_id, "text": text})


@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"


@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]

        if "document" in data["message"]:
            file_id = data["message"]["document"]["file_id"]
            file_info = requests.get(URL + f"getFile?file_id={file_id}").json()
            file_path = file_info["result"]["file_path"]
            file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
            send_message(chat_id, f"Fayl qabul qilindi!\nYuklab olish: {file_url}")
            return {"ok": True}

        if "text" in data["message"]:
            text = data["message"]["text"]
            send_message(chat_id, f"Siz yubordingiz: {text}")

    return {"ok": True}

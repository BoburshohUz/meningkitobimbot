
import os
from flask import Flask, request
import requests

TOKEN = os.getenv("BOT_TOKEN")
app = Flask(__name__)

URL = f"https://api.telegram.org/bot{TOKEN}/"

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]

        requests.post(URL + "sendMessage", json={"chat_id": chat_id, "text": text})

    return "OK", 200

@app.route("/", methods=["GET"])
def home():
    return "Bot is running", 200


import os
from flask import Flask, request
import requests

TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Bot is running", 200

@app.route("/", methods=["POST"])
def webhook():
    data = request.json

    # TEXT message
    if "message" in data:
        msg = data["message"]
        chat_id = msg["chat"]["id"]

        # Text
        if "text" in msg:
            text = msg["text"]
            requests.post(BASE_URL + "sendMessage", json={"chat_id": chat_id, "text": text})

        # File upload (documents)
        if "document" in msg:
            file_id = msg["document"]["file_id"]
            file_info = requests.get(BASE_URL + f"getFile?file_id={file_id}").json()

            if file_info.get("ok"):
                file_path = file_info["result"]["file_path"]
                file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"

                requests.post(BASE_URL + "sendMessage",
                    json={"chat_id": chat_id, "text": f"📁 Fayl qabul qilindi!
Havola:
{file_url}"}
                )

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

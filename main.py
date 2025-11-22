import os
from flask import Flask, request
import requests

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Bot is running", 200

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()

    if not data:
        return "No data", 200

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]

        # If user sends file
        if "document" in data["message"]:
            file_id = data["message"]["document"]["file_id"]

            # Get file link
            file_info = requests.get(f"{BASE_URL}getFile?file_id={file_id}").json()
            file_path = file_info["result"]["file_path"]
            file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"

            # Echo link to user
            requests.post(
                BASE_URL + "sendMessage",
                json={"chat_id": chat_id, "text": f"Fayl yuklandi!\nURL: {file_url}"}
            )

        else:
            # Text message
            text = data["message"].get("text", "")
            requests.post(
                BASE_URL + "sendMessage",
                json={"chat_id": chat_id, "text": "Fayl yuboring 📁"}
            )

    return "OK", 200

if __name__ == "__main__":
    # Set webhook automatically if provided
    if WEBHOOK_URL:
        requests.get(f"{BASE_URL}setWebhook?url={WEBHOOK_URL}")
    app.run(host="0.0.0.0", port=8080)

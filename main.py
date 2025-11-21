
from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.getenv("BOT_TOKEN")
API = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text):
    requests.get(f"{API}/sendMessage", params={"chat_id": chat_id, "text": text})

@app.route("/", methods=["GET"])
def home():
    return "Bot working on Render!"

@app.route("/", methods=["POST"])
def webhook():
    update = request.get_json()
    if not update:
        return "no update"

    if "message" in update:
        msg = update["message"]
        chat_id = msg["chat"]["id"]

        if "document" in msg:
            file_id = msg["document"]["file_id"]
            file_name = msg["document"]["file_name"]

            file_info = requests.get(f"{API}/getFile", params={"file_id": file_id}).json()
            file_path = file_info["result"]["file_path"]

            file_download_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
            file_data = requests.get(file_download_url).content

            os.makedirs("files", exist_ok=True)
            save_path = f"files/{file_name}"

            with open(save_path, "wb") as f:
                f.write(file_data)

            send_message(chat_id, "Fayl muvaffaqiyatli qabul qilindi!")
            return "saved", 200
        else:
            send_message(chat_id, "Menga fayl yubor 😉")

    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

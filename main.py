import os
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = "CGIDJC0VOHYOCZSFQBWZVAYLCQWSWMWMEANNLPRPNGAISNEGDZJDTHJUVEINJZFV"
BASE_URL = f"https://botapi.rubika.ir/v3/{BOT_TOKEN}"

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    print(">>> SUCCESS! WEBHOOK WAS HIT BY RUBIKA! <<<")
    try:
        data = request.get_json(silent=True)
        print("Data received:", data)
        
        if data and "message" in data:
            chat_id = data["message"]["chat_id"]
            text = data["message"].get("text", "")
            print(f"User message: {text}")
            
            if text == "/start":
                send_message(chat_id, "سلام! ربات فعال شد. 🚀")
    except Exception as e:
        print("Error in webhook:", e)
        
    return "OK", 200

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        res = requests.post(url, json=payload)
        print("Send response:", res.text)
    except Exception as e:
        print("Send error:", e)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
  

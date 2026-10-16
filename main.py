import os
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = "CGIDJC0VOHYOCZSFQBWZVAYLCQWSWMWMEANNLPRPNGAISNEGDZJDTHJUVEINJZFV"
BASE_URL = f"https://botapi.rubika.ir/v3/{BOT_TOKEN}"

@app.route('/')
def home():
    return "Bot is running and alive!"

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    print("=== WEBHOOK HIT ===")
    try:
        data = request.get_json(silent=True)
        print("Received data:", data)
        
        if data and "message" in data:
            chat_id = data["message"]["chat_id"]
            text = data["message"].get("text", "")
            print(f"Message from {chat_id}: {text}")
            
            if text == "/start":
                send_message(chat_id, "سلام! ربات ایران نارسیتیف با موفقیت فعال شد. 🚀")
    except Exception as e:
        print("Error handling webhook:", e)
        
    return "OK", 200

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    try:
        response = requests.post(url, json=payload)
        print("Send message response:", response.text)
    except Exception as e:
        print("Error sending message:", e)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
    

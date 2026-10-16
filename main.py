import os
import requests
from flask import Flask, request

app = Flask(__name__)

# توکن ربات روبیکای خودت را جایگزین کن
BOT_TOKEN = "CGIDJC0VOHYOCZSFQBWZVAYLCQWSWMWMEANNLPRPNGAISNEGDZJDTHJUVEINJZFV"
BASE_URL = f"https://botapi.rubika.ir/v3/{BOT_TOKEN}"

@app.route('/')
def home():
    return "Bot is running and alive!"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        print("Received data from Rubika:", data)
        
        if data and "message" in data:
            chat_id = data["message"]["chat_id"]
            text = data["message"].get("text", "")
            
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
    

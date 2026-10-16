import os
import requests
from flask import Flask, request

app = Flask(__name__)

# توکن رباتت را اینجا دقیقاً بین دابل‌کوتیشن قرار بده
BOT_TOKEN = "CGIDJC0VOHYOCZSFQBWZVAYLCQWSWMWMEANNLPRPNGAISNEGDZJDTHJUVEINJZFV"
RUBIKA_API_URL = f"https://botapi.rubika.ir/v3/{BOT_TOKEN}"

@app.route('/')
def home():
    return "Bot is running and alive!"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        print("Received update from Rubika:", data)
        
        # استخراج متن پیام و آیدی کاربر (اگر پیامی آمده باشد)
        if data and 'message' in data:
            message = data['message']
            chat_id = message.get('chat_id')
            text = message.get('text', '')
            
            # اگر کاربر /start فرستاد، جواب بده
            if text == '/start':
                send_message(chat_id, "سلام! ربات ایران نارسیتیف با موفقیت روشن شد و آماده به کار است. 🚀")
                
        return "OK", 200
    except Exception as e:
        print("Error processing webhook:", e)
        return "OK", 200

def send_message(chat_id, text):
    url = f"{RUBIKA_API_URL}/sendMessage"
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

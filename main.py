import os
import json
import time
import threading
import requests
from flask import Flask

# تنظیمات اصلی
TOKEN = os.getenv("BOT_TOKEN", "CGIDJC0VOHYOCZSFQBWZVAYLCQWSWMWMEANNLPRPNGAISNEGDZJDTHJUVEINJZFV")  # توکن ربات روبیکا
API_URL = f"https://botapi.rubika.ir/v3/{TOKEN}"
DB_FILE = "database.json"

app = Flask(__name__)

# مدیریت دیتابیس JSON ساده و ایمن
def load_db():
    if not os.path.exists(DB_FILE):
        return {"users": {}, "admins": []}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"users": {}, "admins": []}

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# ارسال پیام به روبیکا
def send_message(chat_id, text):
    url = f"{API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"Send message response: {response.text}")
    except Exception as e:
        print(f"Error sending message: {e}")

# پردازش پیام‌های دریافتی
def handle_message(message):
    try:
        chat_id = message.get("chat_id")
        text = message.get("text", "").strip()
        sender_id = message.get("sender_id")
        
        if not chat_id or not text:
            return

        print(f"Received message from {sender_id}: {text}")

        db = load_db()
        # ثبت کاربر در دیتابیس
        if sender_id and sender_id not in db["users"]:
            db["users"][sender_id] = {"joined_at": time.time()}
            save_db(db)

        # پاسخ به دستورات
        if text == "/start":
            welcome_text = (
                "سلام! 🇮🇷 به ربات رسمی «ایران روایت» (Iran Narrative) خوش آمدید.\n\n"
                "از منوهای زیر یا دستورات استفاده کنید:"
            )
            send_message(chat_id, welcome_text)
        elif text == "مدیریت" or text == "/panel":
            send_message(chat_id, "پنل مدیریت فعال است.")
        else:
            send_message(chat_id, f"پیام شما دریافت شد: {text}")

    except Exception as e:
        print(f"Error in handle_message: {e}")

# حلقه دریافت پیام (Long Polling در پس‌زمینه)
def run_polling():
    offset = 0
    print("Bot polling started in background thread...")
    time.sleep(3)  # کمی مکث برای بالا آمدن کامل سرور
    
    while True:
        try:
            url = f"{API_URL}/getUpdates"
            payload = {"offset": offset, "limit": 10, "timeout": 30}
            response = requests.post(url, json=payload, timeout=35)
            
            if response.status_code == 200:
                result = response.json()
                updates = result.get("data", {}).get("updates", []) or result.get("updates", [])
                
                for update in updates:
                    # پشتیبانی از ساختارهای مختلف احتمالی آپدیت در روبیکا
                    msg = update.get("message") or update.get("body", {}).get("message")
                    if msg:
                        handle_message(msg)
                    
                    update_id = update.get("update_id") or update.get("id")
                    if update_id is not None:
                        offset = int(update_id) + 1
            else:
                print(f"Polling HTTP error: {response.status_code}")
                
        except Exception as e:
            print(f"Polling exception: {e}")
            
        time.sleep(2)

# وب‌سرویس Flask برای زنده نگه داشتن رندر (Keep-Alive)
@app.route("/")
def index():
    return "Iran Narrative Bot is running successfully!"

# راه‌اندازی ترد پولینگ همراه با Flask
if __name__ == "__main__":
    t = threading.Thread(target=run_polling, daemon=True)
    t.start()
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
              

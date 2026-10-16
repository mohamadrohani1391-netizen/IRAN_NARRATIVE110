import os
import time
from flask import Flask, request
from rubika_api import get_updates, send_message
from logic import handle_message
import threading

app = Flask(__name__)

# مسیر برای رندر که سرور را زنده نگه دارد
@app.route("/", methods=["GET"])
def home():
    return "Bot is Polling...", 200

def bot_loop():
    """حلقه اصلی که مدام پیام‌ها را چک می‌کند"""
    print("Bot loop started...")
    last_update_id = 0
    
    while True:
        updates = get_updates()
        for update in updates:
            # فقط پیام‌های جدید را پردازش کن
            update_id = update.get("update_id")
            if update_id > last_update_id:
                message = update.get("message", {})
                chat_id = message.get("chat_id")
                text = message.get("text", "")
                
                if chat_id and text:
                    print(f"New message from {chat_id}: {text}")
                    handle_message(chat_id, text)
                
                last_update_id = update_id
        
        time.sleep(2)  # ۲ ثانیه صبر کن و دوباره چک کن (برای جلوگیری از بلاک شدن)

if __name__ == "__main__":
    # اجرای حلقه ربات در یک رشته (Thread) جداگانه
    threading.Thread(target=bot_loop, daemon=True).start()
    
    # اجرای سرور Flask برای رندر
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
              

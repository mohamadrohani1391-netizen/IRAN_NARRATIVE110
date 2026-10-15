import time
import threading
from flask import Flask
from config import BOT_TOKEN, PORT
from rubika_api import RubikaAPI
from logic import Reply

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot IRAN NARRATIVE is running successfully!"

def bot_polling():
    print("Bot polling started...")
    bot = RubikaAPI(BOT_TOKEN)
    offset = None
    
    while True:
        try:
            result = bot.get_updates(offset=offset)
            if result and isinstance(result, dict) and result.get("status") == "Active":
                updates = result.get("updates", [])
                for update in updates:
                    update_id = update.get("update_id")
                    offset = update_id + 1
                    
                    message = update.get("message", {})
                    chat_id = message.get("chat_id")
                    text = message.get("text")
                    
                    if chat_id and text:
                        # پردازش پیام از طریق logic.py
                        reply_text = Reply({"chat_id": chat_id, "text": text})
                        if reply_text:
                            bot.send_message(chat_id, reply_text)
            
            time.sleep(3) # مکث کوتاه بین هر چک کردن
        except Exception as e:
            print(f"Error in polling loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    # اجرای ربات در یک ترد جداگانه
    t = threading.Thread(target=bot_polling)
    t.daemon = True
    t.start()
    
    # اجرای وب‌سرور فلاسک برای رندر
    app.run(host="0.0.0.0", port=PORT)
  

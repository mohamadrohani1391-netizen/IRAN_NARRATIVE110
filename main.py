import time
from flask import Flask
from config import BOT_TOKEN, PORT
from rubika_api import RubikaAPI
from logic import Reply

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot IRAN NARRATIVE is running successfully!"

def main():
    print("Bot IRAN NARRATIVE is starting...")
    bot = RubikaAPI(BOT_TOKEN)
    
    # حلقه اصلی اجرای ربات و بررسی آپدیت‌ها
    while True:
        try:
            # در اینجا ارتباط با سرور روبیکا و دریافت پیام‌ها انجام می‌شود
            time.sleep(5)
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    import threading
    # اجرای حلقه ربات در یک ترد جداگانه
    t = threading.Thread(target=main)
    t.daemon = True
    t.start()
    
    # اجرای وب‌سرور فلاسک برای پاسخ به پورت رندر
    app.run(host="0.0.0.0", port=PORT)
  

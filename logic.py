import json
import os

DB_FILE = "database.json"

# بارگذاری یا ساخت دیتابیس اولیه
def load_db():
    if not os.path.exists(DB_FILE):
        default_data = {
            "admins": ["محمد امین روحانی"],
            "passcode": "@IRAN NARRATIVE 313",
            "about": "این ربات متعلق به پروژه IRAN NARRATIVE است.",
            "channel": "هنوز تنظیم نشده است",
            "posts": [],
            "feedback": [],
            "active_admins_session": []
        }
        save_db(default_data)
        return default_data
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

from rubika_api import send_message

def handle_message(chat_id, text):
    db = load_db()
    
    # دستور استارت
    if text == "/start":
        msg = (
            "سلام! به ربات IRAN NARRATIVE خوش آمدید.\n\n"
            "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:\n"
            "📩 ارسال نظرات\n"
            "📂 مشاهده پست‌ها\n"
            "ℹ️ درباره ما\n"
            "🛠 پشتیبانی\n"
            "📢 دریافت کانال\n"
            "منوی ادمین"
        )
        send_message(chat_id, msg)
        return

    # ورود به منوی ادمین
    if text == "منوی ادمین":
        send_message(chat_id, "لطفاً رمز عبور ادمین را ارسال کنید:")
        return

    # بررسی رمز ادمین
    if text == db.get("passcode"):
        db["active_admins_session"].append(chat_id)
        save_db(db)
        send_message(chat_id, "خوش آمدید ادمین عزیز!\nبه منوی مدیریت خوش آمدید.")
        return

    # پاسخ به دکمه‌های کاربران
    if text == "ℹ️ درباره ما":
        send_message(chat_id, db.get("about", "توضیحی ثبت نشده است."))
    elif text == "📢 دریافت کانال":
        send_message(chat_id, f"کانال رسمی پروژه: {db.get('channel', 'تنظیم نشده')}")
    elif text == "📩 ارسال نظرات":
        send_message(chat_id, "لطفاً نظر، انتقاد یا پیشنهاد خود را ارسال کنید تا به دست مدیریت برسد.")
    else:
        # اگر پیام عادی بود (مثلاً نظر کاربر)
        if chat_id not in db.get("active_admins_session", []):
            db["feedback"].append({"chat_id": chat_id, "text": text})
            save_db(db)
            send_message(chat_id, "پیام شما با موفقیت به ادمین ارسال شد. ممنون از نظرتان!")
        else:
            send_message(chat_id, "دستور نامعتبر یا ثبت شده در سیستم.")
      

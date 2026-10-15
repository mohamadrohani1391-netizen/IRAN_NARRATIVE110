import json
import os

DB_FILE = "database.json"

def load_database():
    if not os.path.exists(DB_FILE):
        default_data = {
            "users": [],
            "admins": [
                {
                    "name": "محمد امین روحانی",
                    "passcode": "@IRAN NARRATIVE 313"
                }
            ],
            "posts": [],
            "feedback": [],
            "settings": {
                "bot_name": "ربات ایران نریتیو",
                "about": "تیم IRAN NARRATIVE - فعال در حوزه تولید محتوا، بازی‌های متنی و مدیریت کانال.",
                "channel_text": "لینک کانال رسمی: https://rubika.ir/iran_narrative"
            }
        }
        save_database(default_data)
        return default_data
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"users": [], "admins": [], "posts": [], "feedback": [], "settings": {}}

def save_database(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
  

import os
import requests
import time

BOT_TOKEN = os.environ.get("BOT_TOKEN", "توکن_خودت_را_اینجا_بگذار")

def send_message(chat_id, text):
    url = f"https://bot.rubika.ir/v0/{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        requests.post(url, json=payload, timeout=10)
    except:
        pass

def get_updates():
    """این تابع به جای وب‌هوک، خودش دنبال پیام می‌گردد"""
    url = f"https://bot.rubika.ir/v0/{BOT_TOKEN}/getUpdates"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json().get("result", [])
    except Exception as e:
        print(f"Error getting updates: {e}")
    return []
  

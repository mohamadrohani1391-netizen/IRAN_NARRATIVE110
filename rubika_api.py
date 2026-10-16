import requests
from config import BOT_TOKEN

# آدرس پایه رسمی API روبیکا (نسخه v3)
BASE_URL = f"https://botapi.rubika.ir/v3/{BOT_TOKEN}"

def get_updates(offset=0):
    """گرفتن پیام‌های جدید از روبیکا با متد v3"""
    try:
        url = f"{BASE_URL}/getUpdates"
        payload = {"offset": offset, "limit": 10, "timeout": 30}
        response = requests.post(url, json=payload, timeout=35)
        if response.status_code == 200:
            return response.json().get("result", [])
    except Exception as e:
        print(f"Error getting updates: {e}")
    return []

def send_message(chat_id, text):
    """ارسال پیام به کاربر با متد v3"""
    try:
        url = f"{BASE_URL}/sendMessage"
        payload = {"chat_id": chat_id, "text": text}
        response = requests.post(url, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Error sending message: {e}")
        return None
      

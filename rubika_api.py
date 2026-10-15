import requests

class RubikaAPI:
    def __init__(self, token):
        self.token = token
        self.base_url = f"https://bot.rubika.ir/v1/{token}"

    def send_message(self, chat_id, text, keyboard=None):
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text
        }
        if keyboard:
            payload["reply_markup"] = keyboard
        try:
            response = requests.post(url, json=payload, timeout=10)
            return response.json()
        except Exception as e:
            print(f"Error sending message: {e}")
            return None
          

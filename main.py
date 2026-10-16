import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running and alive!"

@app.route('/webhook', methods=['POST'])
def webhook():
    # دریافت داده‌های ارسالی از روبیکا
    data = request.get_json()
    print("Received data:", data)
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
  

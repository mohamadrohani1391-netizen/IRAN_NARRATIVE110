import os

# خواندن توکن و پورت از متغیرهای محیطی هاست
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
PORT = int(os.environ.get("PORT", 5000))

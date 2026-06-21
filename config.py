import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.environ.get("API_ID", "12345"))
    API_HASH = os.environ.get("API_HASH", "your_hash")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_token")
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "YourBotName")
    
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", "")
    ADMINS = [int(x) for x in os.environ.get("ADMINS", "12345678").split()]
    
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-100"))
    FILE_STORE_ID = int(os.environ.get("FILE_STORE_ID", "-100"))
    FSUB_CHANNEL = int(os.environ.get("FSUB_CHANNEL", "-100"))
    
    BOT_LOGO = os.environ.get("BOT_LOGO", "https://graph.org/file/your-logo.jpg")
    CH1 = os.environ.get("CH1", "https://t.me/channel1")
    CH2 = os.environ.get("CH2", "https://t.me/channel2")
    CH3 = os.environ.get("CH3", "https://t.me/channel3")
    CH4 = os.environ.get("CH4", "https://t.me/channel4")
    
    URL = os.environ.get("URL", "https://your-app.koyeb.app")
    PORT = int(os.environ.get("PORT", "8080"))
    AUTO_DELETE_TIME = 600 # ১০ মিনিট

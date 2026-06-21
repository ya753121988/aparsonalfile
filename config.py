import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.environ.get("API_ID", "29904834"))
    API_HASH = os.environ.get("API_HASH", "8b4fd9ef578af114502feeafa2d31938")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "8714836567:AAHigOewrnnEzzDRw9Wzxogu2lCsNeHhkAs")
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "YtLiveV2Bot")
    
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", "mongodb+srv://hepemo5263:hepemo5263@cluster0.5vugv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    ADMINS = [int(x) for x in os.environ.get("ADMINS", "7120801813").split()]
    
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1004498638459"))
    FILE_STORE_ID = int(os.environ.get("FILE_STORE_ID", "-1004498638459"))
    FSUB_CHANNEL = int(os.environ.get("FSUB_CHANNEL", "-1004498638459"))
    
    BOT_LOGO = os.environ.get("BOT_LOGO", "https://graph.org/file/your-logo.jpg")
    CH1 = os.environ.get("CH1", "https://t.me/channel1")
    CH2 = os.environ.get("CH2", "https://t.me/channel2")
    CH3 = os.environ.get("CH3", "https://t.me/channel3")
    CH4 = os.environ.get("CH4", "https://t.me/channel4")
    
    # এখানে https:// যোগ করা হয়েছে, এটি ছাড়া রেন্ডারে কাজ করবে না
    URL = os.environ.get("URL", "https://aparsonalfile.onrender.com") 
    PORT = int(os.environ.get("PORT", "8080"))
    AUTO_DELETE_TIME = 600 # ১০ মিনিট

import motor.motor_asyncio
from config import Config

class Database:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(Config.MONGO_DB_URI)
        self.db = self.client["FileBotDB"]
        self.users = self.db["users"]
        self.settings = self.db["settings"]

    async def add_user(self, user_id):
        await self.users.update_one({"id": user_id}, {"$set": {"id": user_id}}, upsert=True)

    async def set_watermark(self, text):
        await self.settings.update_one({"id": "watermark"}, {"$set": {"text": text}}, upsert=True)

    async def get_watermark(self):
        data = await self.settings.find_one({"id": "watermark"})
        return data["text"] if data else "@YourBot"

db = Database()

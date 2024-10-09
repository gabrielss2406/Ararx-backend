from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure

class MongoDB:
    def __init__(self, uri: str, db_name: str):
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self.db = None

    # func pra conectar
    async def connect(self):
        try:
            self.client = AsyncIOMotorClient(self.uri)
            self.db = self.client[self.db_name]
            await self.db.command("ping")
            print("Successfully connected to MongoDB!")
        except ConnectionFailure as e:
            print(f"Failed to connect to MongoDB: {e}")
            raise
    # func pra desconectar
    async def close(self):
        if self.client:
            self.client.close()
            print("MongoDB connection closed.")


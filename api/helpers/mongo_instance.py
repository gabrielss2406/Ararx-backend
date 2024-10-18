from dotenv import load_dotenv
import os
from api.services.db.database import MongoDB

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

mongo = MongoDB(MONGO_URI, "ararx")

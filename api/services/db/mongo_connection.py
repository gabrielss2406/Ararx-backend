import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(
    MONGO_URI,
    maxPoolSize=50,
    minPoolSize=5
)


def connect_mongo(collection_name: str) -> tuple[Collection, MongoClient]:
    try:
        db: Database = client['ararx']
        collection: Collection = db[collection_name]
        print("Conexão estabelecida com sucesso.")
        return collection, client
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        raise

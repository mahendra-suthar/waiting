from fastapi import FastAPI
from pymongo import MongoClient
# from motor.motor_asyncio import AsyncIOMotorClient

from .config import MONGODB_CONNECTION_URI, DB_NAME

app = FastAPI()

client = MongoClient(MONGODB_CONNECTION_URI)
client_db = client[DB_NAME]


# MongoDB connection
# def get_db():
#     try:
#         mongo_client = MongoClient(MONGODB_CONNECTION_URI)
#         database = mongo_client[DB_NAME]
#         yield database
#     finally:
#         client.close()

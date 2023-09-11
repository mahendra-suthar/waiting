from fastapi import FastAPI
from pymongo import MongoClient

from .config import MONGODB_CONNECTION_URI, DB_NAME

app = FastAPI()

# MongoDB connection
client = MongoClient(MONGODB_CONNECTION_URI)
client_db = client[DB_NAME]

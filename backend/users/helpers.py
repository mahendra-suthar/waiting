import pymongo
from fastapi import HTTPException
from pymongo.errors import WriteError

from logs import logger as log
from config.database import client_db

user_collection = client_db['users']
# user_collection.create_index([("email", pymongo.ASCENDING), ("phone_number", pymongo.ASCENDING)], unique=True)


def insert_user(user):
    """
    Add user
    """
    try:
        user_obj = user_collection.insert_one(user)
        if user_obj:
            return user_obj.inserted_id
        else:
            log.error(f"User not found after insertion")
            raise HTTPException(status_code=409, detail="User not found after insertion")
    except Exception as e:
        log.error(f"Error while inserting a user into the database: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")



import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


MONGODB_CONNECTION_URI = os.environ.get('MONGODB_CONNECTION_URI')
DB_NAME = os.environ.get('MONGODB_DATABASE')

TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')

REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
REDIS_DB = os.environ.get('REDIS_DB')

ACCESS_TOKEN_EXPIRE_DAYS = os.environ.get('ACCESS_TOKEN_EXPIRE_DAYS')

BACKED_SERVER = os.environ.get('BACKED_SERVER')

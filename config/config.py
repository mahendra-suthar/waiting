import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


MONGODB_CONNECTION_URI = os.environ.get('MONGODB_CONNECTION_URI')
DB_NAME = os.environ.get('DB_NAME')

TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')

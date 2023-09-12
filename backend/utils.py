import pyotp
import random
from fastapi import HTTPException
from twilio.rest import Client

from config.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
from config.redis import redis_client
from logs import logger as log


def success_response(data=None, message=None):
    return_data = dict()
    return_data["data"] = data
    return_data["success"] = True
    return_data["message"] = message
    return return_data


def error_response(data=None, error=None):
    return_data = dict()
    return_data["data"] = data
    return_data["success"] = False
    return_data["error"] = error
    return return_data


# Generate a random 6-digit OTP
def generate_otp():
    return str(random.randint(1000, 9999))


# Function to generate and store OTP secret for a user
def generate_and_store_otp_secret(phone_number):
    """
    Generate OTP using pyotp and store OTP into redis database
    """
    
    otp_secret = pyotp.random_base32()
    totp = pyotp.TOTP(otp_secret, digits=6)
    otp_code = totp.now()

    print(f"Generated OTP: {otp_code}")
    try:
        redis_client.setex(phone_number, 60, otp_secret)
    except Exception as e:
        log.error(f"Error while store OTP: {e}")
        return False
    return True


# Verify OTP
def verify_otp(phone_number, otp_code):
    """
    Verify OTP
    """
    try:
        otp_secret = redis_client.get(phone_number)
        print("------otp_secret-------", otp_secret)
        if otp_secret:
            totp = pyotp.TOTP(otp_secret)
            print("------totp.verify(otp_code)-------", totp.verify(otp_code))
            return totp.verify(otp_code)
        else:
            return False
    except Exception as error:
        log.error(f"Error while verify OTP: {error}")
        return False


# Send OTP via SMS using Twilio
def send_otp_via_sms(phone_number, otp):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your OTP is: {otp}",
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    return message

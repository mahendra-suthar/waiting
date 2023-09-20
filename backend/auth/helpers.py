import jwt
from fastapi import HTTPException
from datetime import datetime, timedelta
from fastapi.encoders import jsonable_encoder

from logs import logger as log
from config.database import client_db
from backend.users.helpers import insert_user_request
from config.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from ..utils import success_response, temp_gen_otp_and_store, temp_verify_otp

user_collection = client_db['users']


def send_phone_otp(user):
    """
    Send OTP to phone number via sms
    """
    try:
        phone_number = user.get("phone_number", None)
        if phone_number:
            # sent = generate_and_store_otp_secret(phone_number)
            sent = temp_gen_otp_and_store(phone_number)
            if sent:
                return success_response(message="Successfully send OTP")
            else:
                raise HTTPException(status_code=409, detail="Something went wrong during save OTP")
        else:
            raise HTTPException(status_code=409, detail="Please enter valid phone number")
    except Exception as e:
        log.error(f"Error while send OTP to phone number: {e}")
        raise HTTPException(status_code=500, detail="Error while send OTP to phone number")


def verify_phone_otp_and_login(user):
    """
    Verify OTP and Login or Register using phone number OTP
    """
    try:
        phone_number = user.get("phone_number", None)
        otp = user.get("otp", None)
        if phone_number:
            if temp_verify_otp(phone_number, otp):
                user_obj = user_collection.find_one({'phone_number': phone_number})
                if not user_obj:
                    user_id = insert_user_request({'phone_number': phone_number})
                else:
                    user_id = str(user_obj['_id'])
                token = create_jwt_token(user_id)
                return_data = {
                    'token': token,
                    'user': jsonable_encoder(user_obj)
                }
                return return_data
            else:
                raise HTTPException(status_code=400, detail="OTP is not valid")
        else:
            raise HTTPException(status_code=409, detail="Please enter valid phone number")
    except Exception as e:
        log.error(f"Error while verify OTP for phone number: {e}")
        raise HTTPException(status_code=500, detail="Error while verify OTP for phone number")


# Function to generate JWT token
def create_jwt_token(user_id: any):
    try:
        if user_id:
            payload = {
                "sub": str(user_id),
                "exp": datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        else:
            raise HTTPException(status_code=400, detail="Invalid token data")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token data")
    except Exception as e:
        log.error(f"Error while creating JWT token: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return token




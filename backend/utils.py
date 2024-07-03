import os
from fastapi import Response, Request
from io import BytesIO
import bcrypt
import qrcode
import qrcode.constants
import pyotp
import random
from datetime import datetime
from twilio.rest import Client
from typing import List
from PIL import Image

from config.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
from config.redis import redis_client
from logs import logger as log
from config.database import client_db


def success_response(status=200, data=None, message=None):
    return_data = dict()
    return_data["data"] = data
    return_data["status"] = status
    return_data["success"] = True
    return_data["message"] = message
    return return_data


def error_response(status=500, data=None, error=None):
    return_data = dict()
    return_data["data"] = data
    return_data["status"] = status
    return_data["success"] = False
    return_data["error"] = error
    return return_data


# Generate a random 6-digit OTP
def generate_otp():
    return str(random.randint(1000, 9999))


def temp_gen_otp_and_store(phone_number):
    try:
        # redis_client.setex(phone_number, 30, 123456)
        otp = 123456
    except Exception as e:
        log.error(f"Error while store OTP: {e}")
        return False
    return True


def temp_verify_otp(phone_number, otp_code):
    try:
        # otp = redis_client.get(phone_number)

        if int(otp_code):
            # redis_client.delete(phone_number)
            return True
        else:
            return False
    except Exception as e:
        log.error(f"Error while store OTP: {e}")
        return False


# Function to hash a password
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

# Function to verify a password against a hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def save_cookies(response: Response, key, value):
    response.set_cookie(key='access_token', value=value)

def get_cookies(request: Request, key):
    return request.cookies.get(key)


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
        send_otp_via_sms(phone_number, otp_code)
    except Exception as e:
        log.error(f"Error while sending OTP: {e}")
        return False
    try:
        redis_client.setex(phone_number, 30, otp_secret)
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
        if otp_secret:
            totp = pyotp.TOTP(otp_secret.decode('utf-8'))  # Convert bytes to str
            is_verify = totp.verify(otp_code)
            if is_verify:
                # Remove the OTP secret from Redis after successful verification
                redis_client.delete(phone_number)
                return True
            else:
                return False
        else:
            return False
    except (pyotp.otp.InvalidToken, pyotp.otp.ExpiredToken, pyotp.otp.InvalidBase32) as otp_error:
        log.error(f"Error during OTP verification: {otp_error}")
        return False
    except Exception as error:
        log.error(f"Unexpected error during OTP verification: {error}")
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


def get_current_timestamp_utc():
    current_utc_timestamp = int(datetime.utcnow().timestamp())
    return current_utc_timestamp

def get_current_date_str(utc_timestamp=None):
    if not utc_timestamp:
        utc_timestamp = get_current_timestamp_utc()

    # Convert the UTC timestamp to a datetime object
    utc_datetime = datetime.utcfromtimestamp(utc_timestamp)

    # Format the datetime object as a string
    formatted_date = utc_datetime.strftime("%d-%m-%Y")  # Change the format as needed
    return formatted_date


def prepare_dropdown_for_forms(collection_name: str, label: str, value: str):
    from .queries import generate_mongo_query
    try:
        query, projections = generate_mongo_query({'is_deleted': False}, projection_fields=[label, value])
        database = client_db
        collection = database[collection_name]
        result = collection.find(query, projections)
        documents = [(str(doc[value]), doc[label]) for doc in result if doc.get(value)]
        documents = [(None, 'Select Item...')] + documents
        return documents
    except Exception as error:
        log.error(f"Something went wrong during prepare_dropdown_data: {error}")
        return []


def prepare_dropdown_data(
        collection_name: str,
        label: str,
        value: str,
        filters: dict = None
) -> List:
    from .queries import generate_mongo_query
    if filters is None:
        filters = dict()

    filters['is_deleted'] = False
    try:
        query, projections = generate_mongo_query(filters, projection_fields=[label, value])
        database = client_db
        collection = database[collection_name]
        result = collection.find(query, projections)
        documents = [{'value': str(doc[value]), 'label': doc[label]} for doc in result if doc.get(value)]
        return documents
    except Exception as error:
        log.error(f"Something went wrong during prepare_dropdown_data: {error}")
        return []


def prepare_static_choice_dropdown(choices):
    choice_list = [(int(value), label) for value, label in choices]
    choice_list = [(None, 'Select Item...')] + choice_list
    return choice_list

# def prepare_static_choice_dict(choices):
#     choice_list = [(int(value), label) for value, label in choices]
#     return choice_list


# async def save_uploaded_file(img: any) -> str:
#     file_name = f"qr_{get_current_timestamp_utc()}.png"
#     file_path = f"/qr-code/{file_name}"  # Update the path as needed
#     img.save(f"/app/{file_path}")
#     return file_path


def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    file_name = f"qr_{get_current_timestamp_utc()}.png"
    file_path = f"/qr-code/{file_name}"  # Update the path as needed
    img.save(f"/app/{file_path}")
    return file_path


# def generate_qr_code_with_logo(data, logo_path):
#     try:
#         # Generate the QR code
#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_L,
#             box_size=10,
#             border=4,
#         )
#         qr.add_data(data)
#         qr.make(fit=True)
#         qr_image = qr.make_image(fill_color="black", back_color="white").convert('RGBA')
#         print("QR image created:", qr_image)
#
#         # Load the business logo
#         with open(logo_path, "rb") as f:
#             logo_data = f.read()
#         logo = Image.open(BytesIO(logo_data))
#         print("Logo image opened:", logo)
#
#         # Calculate the position to place the logo in the center of the QR code
#         # qr_width, qr_height = qr_image.size
#         # logo_width, logo_height = logo.size
#         # position = ((qr_width - logo_width) // 2, (qr_height - logo_height) // 2)
#
#         # Calculate the position to place the logo in the center of the QR code
#         qr_width, qr_height = qr_image.size
#         logo_width, logo_height = logo.size
#         # Ensure the logo is not placed outside the boundaries of the QR code image
#         x_offset = max(0, (qr_width - logo_width) // 2)
#         y_offset = max(0, (qr_height - logo_height) // 2)
#         position = (x_offset, y_offset)
#         print("Position calculated:", position)
#
#
#         # Paste the logo onto the QR code
#         qr_image.paste(logo, position, logo)
#         print("Logo pasted onto QR image")
#
#         # Save the resulting image
#         file_name = f"qr_{get_current_timestamp_utc()}.png"
#         file_path = f"/qr-code/{file_name}"  # Update the path as needed
#         qr_image.save(f"/app/{file_path}")
#         print("QR code with logo saved:", file_path)
#
#         return file_path
#
#     except Exception as error:
#         log.error(f"Something went wrong during generate_qr_code_with_logo: {error}")
#         return ''

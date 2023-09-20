from fastapi.routing import APIRouter
from fastapi import Body, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from .schema import SendOTP, VerifyOTP
from models.users import User
from logs import logger as log
from .helpers import send_phone_otp, verify_phone_otp_and_login
from ..utils import success_response

router = APIRouter()


@router.post("/v1/send_otp", response_description="Send OTP to phone number", response_model=User)
async def send_otp(send_otp_body: SendOTP = Body(...)):
    """
    Send OTP using phone number
    """
    send_otp_data = jsonable_encoder(send_otp_body)
    return_data = send_phone_otp(send_otp_data)
    return JSONResponse(content=return_data, status_code=201)


@router.post("/v1/verify_otp", response_description="Verif OTP and Login using phone number", response_model=User)
async def login_with_phone(verify_otp: VerifyOTP = Body(...)):
    """
    Verif OTP and Login using phone number
    """
    verify_otp_data = jsonable_encoder(verify_otp)
    return_data = verify_phone_otp_and_login(verify_otp_data)
    response_data = success_response(data=return_data, message="Login Successfully")
    return JSONResponse(content=response_data, status_code=201)



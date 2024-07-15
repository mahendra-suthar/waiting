from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from datetime import datetime, timedelta
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer
from fastapi.requests import Request

from logs import logger as log
from config.database import client_db
from ..users.helpers import insert_user_request
from config.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_DAYS
from ..utils import success_response, temp_gen_otp_and_store, temp_verify_otp
from ..queries import insert_item, update_item, filter_data, get_item, prepare_item_list
from ..constants import MERCHANT, EMPLOYEE

collection_name = 'users'
user_collection = client_db['users']
business_collection = client_db['business']
employee_collection = client_db['employee']
# oauth2_scheme = OAuth2PasswordBearer(
#     tokenUrl="api/v1/verify_otp"
# )


def register_and_send_phone_otp(user):
    """
    Send OTP to phone number via sms
    """
    try:
        phone_number = user.get("phone_number", None)
        if phone_number:
            is_exist = filter_data(collection_name, {'is_deleted': False, 'phone_number': phone_number})
            if not is_exist:
                # sent = generate_and_store_otp_secret(phone_number)
                insert_item('users', item_data=user)

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
                    raise HTTPException(status_code=400, detail="User does not exist")

                user_id = str(user_obj['_id'])
                user_obj['_id'] = user_id

                business_dict = {
                    'collection_name': 'business',
                    'schema': ['name', 'category_id', 'phone', 'email', 'country_code', "address_id", 'about_business',
                                'phone_number', 'qr_code']
                }
                business_response = prepare_item_list(business_dict)
                business_list = business_response.get('data', [])

                employee_list_dict = {
                    'collection_name': 'employee',
                    'schema': ['email', 'phone_number', 'country_code', 'employee_number', 'user_id', 'queue_id',
                               'qr_code', 'merchant_id'],
                }
                employees_response = prepare_item_list(employee_list_dict)
                employee_list = employees_response.get('data', [])

                business_data_dict = {business['_id']: {**business} for business in business_list if business}
                employee_dict = {employee['_id']: {**employee} for employee in employee_list if employee}

                user_list_dict = {
                    'collection_name': 'users',
                    'schema': ['employee_id', 'full_name']
                }
                user_response = prepare_item_list(user_list_dict)
                user_list = user_response.get('data', [])
                user_dict = {user['_id']: {**user} for user in user_list if user}

                if user_obj['user_type']:
                    business_obj = business_collection.find_one({'owner_id': user_id})
                    if business_obj:
                        user_obj['business_id'] = str(business_obj['_id'])
                        user_obj['business_details'] = business_data_dict[str(business_obj['_id'])]
                    employee_obj = employee_collection.find_one({'user_id': user_id})
                    if employee_obj:
                        user_obj['employee_id'] = str(employee_obj['_id'])
                        user_obj['employee_details'] = {
                            **employee_dict[str(employee_obj['_id'])],
                            'employee_name': user_dict.get(employee_obj['user_id'], {}).get("full_name"),
                            'employee_business': business_data_dict.get(
                                employee_obj.get('merchant_id'), None
                            )
                        }

                token = create_jwt_token(user_id)
                return_data = {
                    'token': token,
                    'user': jsonable_encoder(user_obj)
                }
                return success_response(data=return_data, message="Successfully logged in")
            else:
                raise HTTPException(status_code=400, detail="OTP is not valid")
        else:
            raise HTTPException(status_code=409, detail="Please enter valid phone number")
    except Exception as e:
        log.error(f"Error while verifying OTP: {e}")
        raise HTTPException(status_code=500, detail=f"Error while verify OTP for phone number")


# Function to generate JWT token
def create_jwt_token(user_id: any):
    try:
        if user_id:
            payload = {
                "sub": str(user_id),
                "exp": datetime.utcnow() + timedelta(days=int(ACCESS_TOKEN_EXPIRE_DAYS))
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


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None


def get_current_user(token: str):
    if token is None:
        raise HTTPException(status_code=401, detail="Token authentication failed")
    username: str = decode_token(token)
    if username is None:
        raise HTTPException(status_code=401, detail="Token authentication failed")
    return username


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            current_user = get_current_user(credentials.credentials)
            if not current_user:
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            return current_user
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")





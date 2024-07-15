from bson import ObjectId, errors
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import Body, HTTPException, Depends
from fastapi.routing import APIRouter
from typing import Any, Optional

from config.database import client_db
from ..utils import success_response, generate_qr_code
from .schema import RegisterEmployee, EmployeeData
from ..queries import insert_item, prepare_item_list, filter_data, update_item, get_item, get_item_list
from ..constants import EMPLOYEE, queue_user_status_choices
from ..auth.helpers import JWTBearer
from .helpers import prepare_employee_queue_history, prepare_employee_queue_history_as_per_status

router = APIRouter()
employee_collection = 'employee'
user_collection = 'users'
business_collection = 'business'
queue_collection = 'queue'
queue_user_collection = 'queue_user'


@router.post("/v1/employee", response_description="Add new Employee")
def create_employee(employee: RegisterEmployee = Body(...), current_user: str = Depends(JWTBearer())) -> Any:
    """
    Register employee api
    """
    employee_data = jsonable_encoder(employee)
    user_id = employee_data.get("user_id")
    try:
        user_id = ObjectId(user_id)
    except errors.InvalidId:
        raise HTTPException(status_code=400, detail="Invalid object")

    email = employee_data.get("email")
    phone_number = employee_data.get("phone_number")
    if email:
        email_exist = filter_data(collection_name='users', filter_dict={'_id': email})
        if email_exist:
            raise HTTPException(status_code=400, detail="Email already exist")

    if phone_number:
        phone_exist = filter_data(collection_name='users', filter_dict={'_id': phone_number})
        if phone_exist:
            raise HTTPException(status_code=400, detail="Phone Number already exist")

    if user_id:
        user_exist = filter_data(collection_name='users', filter_dict={'_id': ObjectId(user_id)})
        if not user_exist:
            raise HTTPException(status_code=400, detail="User not found")

    employee_data['qr_code'] = None
    inserted_employee = insert_item(employee_collection, employee_data, current_user)

    if inserted_employee and user_id:
        update_item(user_collection, str(user_id), {'user_type': EMPLOYEE})

        qr_file_path = generate_qr_code(str(inserted_employee))
        update_item(employee_collection, str(inserted_employee), {'qr_code': qr_file_path})
    response_data = success_response(data={'employee_id': str(inserted_employee)}, message="Successfully inserted data")
    return JSONResponse(content=response_data, status_code=201)


@router.get("/v1/employee", response_description="Get all employees", dependencies=[Depends(JWTBearer())])
async def get_employees(
        page_number: int = 1,
        page_size: int = 10,
        search_string: str = None,
        status: int = None
) -> Any:
    """
    Get all Users
    """
    data_dict = {
        'collection_name': employee_collection,
        'schema': EmployeeData,
        'page_number': page_number,
        'page_size': page_size,
        'search_string': search_string
    }
    print("-------status----", status, type(status))
    if status:
        data_dict['filters'] = {'status': int(status)}

    response_data = prepare_item_list(data_dict)
    data = response_data.get("data")

    user_data = get_item_list(collection_name=user_collection, columns=['full_name'])
    user_data_list = user_data.get('data', [])
    user_dict = {str(user['_id']): user['full_name'] for user in user_data_list if user}

    for item in data:
        item['full_name'] = user_dict.get(item['user_id'])

    status_code = response_data.get("status")
    return JSONResponse(content=response_data, status_code=status_code)


# @router.get("/v1/employee_queue", response_description="Employee's queue details")
# def current_users_appointments(current_user: str = Depends(JWTBearer())) -> Any:
#     """
#     Preparing employee's queue details
#     """
#     employee_list = prepare_item_list({
#         'collection_name': 'employee',
#         'schema': ['user_id', 'queue_id'],
#         'filters': {'is_deleted': False, 'user_id': current_user}
#     })
#     print("------employee_list------", employee_list)
#     data_dict = prepare_employee_queue_history(employee_list.get('data', [])[0])
#     response_data = success_response(data=data_dict['data'], message="Successfully get data")
#     return JSONResponse(content=response_data, status_code=201)


@router.get("/v1/employee_queue_appointments", response_description="Get queue user as per status")
def current_users_appointments(status: Optional[int], current_user: str = Depends(JWTBearer())) -> Any:
    """
    Preparing employee's queue details
    """
    employee_list = prepare_item_list({
        'collection_name': 'employee',
        'schema': ['user_id', 'queue_id'],
        'filters': {'is_deleted': False, 'user_id': current_user}
    })
    employee_details = employee_list.get('data', [])[0] if len(employee_list.get('data', [])) > 0 else {}
    data_dict = {
        'queue_id': employee_details.get('queue_id'),
        'status': status
    }
    data_dict = prepare_employee_queue_history_as_per_status(data_dict)
    response_data = success_response(data=data_dict['data'], message="Successfully get data")
    return JSONResponse(content=response_data, status_code=201)


@router.get("/v1/employee_queue_appointments/{employee_id}", response_description="Get queue user appointments")
def current_users_appointments(employee_id: str, status: int) -> Any:
    """
    Preparing employee's queue appointments
    """
    response_data = get_item(
        collection_name=employee_collection,
        item_id=employee_id,
        columns=['queue_id']
    )
    data = response_data.get("data")
    data_dict = {
        'queue_id': data.get("queue_id"),
        'status': status
    }
    data_dict = prepare_employee_queue_history_as_per_status(data_dict)
    response_data = success_response(data=data_dict['data'], message="Successfully get data")
    return JSONResponse(content=response_data, status_code=201)


# @router.get("/v1/get_employee_using_service", response_description="Get employee using service")
# def current_users_appointments(service_id: str) -> Any:
#     """
#     Preparing employee list as per service
#     """
#     employee_list_dict = {
#         'collection_name': employee_collection,
#         'schema': ['merchant_id'],
#         'filters': {'merchant_id': business_id}
#     }
#     employee_response = prepare_item_list(employee_list_dict)
#     employee_list = [employee['_id'] for employee in employee_response.get('data', []) if employee]
#
#
#     data = response_data.get("data")
#     data_dict = {
#         'queue_id': data.get("queue_id"),
#         'status': status
#     }
#     data_dict = prepare_employee_queue_history_as_per_status(data_dict)
#     response_data = success_response(data=data_dict['data'], message="Successfully get data")
#     return JSONResponse(content=response_data, status_code=201)


@router.get("/v1/employee/{employee_id}", response_description="Get employee")
def get_employee_details(employee_id: str) -> Any:
    """
    Get employee details
    """
    response_data = get_item(
        collection_name=employee_collection,
        item_id=employee_id,
        columns=[
            'merchant_id', 'joined_date', 'email', 'country_code', 'phone_number', 'status', 'user_id', 'queue_id',
        ]
    )
    status_code = response_data.get("status")
    data = response_data.get("data")
    merchant_id = data.get("merchant_id")
    # user_id = data.get("user_id")
    queue_id = data.get("queue_id")
    if merchant_id:
        merchant_data = get_item(
            collection_name=business_collection,
            item_id=merchant_id,
            columns=['name', 'email', 'country_code', 'phone_number', 'status', 'category_id', 'owner_id']
        )
        data['business_details'] = merchant_data.get("data")

    # if user_id:
    #     user_data = get_item(
    #         collection_name=user_collection,
    #         item_id=user_id,
    #         columns=['full_name', 'email', 'country_code', 'phone_number', 'status', 'user_type']
    #     )
    #     data['user_details'] = user_data.get("data")

    if queue_id:
        queue_data = get_item(
            collection_name=queue_collection,
            item_id=queue_id,
            columns=['name', 'limit', 'current_user', 'current_length', 'status']
        )
        data['queue_details'] = queue_data.get('data')

    response_data['data'] = data
    return JSONResponse(content=response_data, status_code=status_code)


@router.get("/v1/employee_queue_status_count/{queue_id}", response_description="Get employee queue status count")
def get_employee_queue_status_count(queue_id: str) -> Any:
    """
    Get employee queue status count
    """
    pipeline = [
        {
            "$match": {
                "is_deleted": False,
                "queue_id": queue_id
            }
        },
        {
            "$group": {
                "_id": "$status",
                "queue_user": {"$sum": 1}
            }
        }
    ]
    grouped_queue_user = client_db[queue_user_collection].aggregate(pipeline)
    queue_user_status_dict = dict(queue_user_status_choices)
    status_count_dict = {
        queue_user_status_dict[queue['_id']]: queue.get('queue_user')
        for queue in grouped_queue_user
    }
    response_data = success_response(data={'status_count_dict': status_count_dict}, message="Successfully get data")
    return JSONResponse(content=response_data, status_code=200)


# @router.put("/v1/employee", response_description="Update Employee")
# def create_employee(employee: RegisterEmployee = Body(...)) -> Any:
#     """
#     Register employee api
#     """
#     employee_data = jsonable_encoder(employee)
#     # inserted_employee = await insert_employee_request(employee_data)
#     inserted_employee = insert_item(employee_collection, employee_data)
#     response_data = success_response(data={'employee_id': str(inserted_employee)}, message="Successfully inserted data")
#     return JSONResponse(content=response_data, status_code=201)



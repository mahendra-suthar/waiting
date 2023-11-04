from bson import ObjectId, errors
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import Body, HTTPException
from fastapi.routing import APIRouter
from typing import Any

from ..utils import success_response
from .schema import RegisterEmployee, EmployeeData
from ..queries import insert_item, prepare_item_list, filter_data

router = APIRouter()
employee_collection = 'employee'


@router.post("/v1/employee", response_description="Add new Employee")
def create_employee(employee: RegisterEmployee = Body(...)) -> Any:
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

    inserted_employee = insert_item(employee_collection, employee_data, )
    response_data = success_response(data={'employee_id': str(inserted_employee)}, message="Successfully inserted data")
    return JSONResponse(content=response_data, status_code=201)


@router.get("/v1/employee", response_description="Get all employees")
async def get_employees(
        page_number: int = 1,
        page_size: int = 10,
        search_string: str = None
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
    response_data = prepare_item_list(data_dict)
    status_code = response_data.get("status")
    return JSONResponse(content=response_data, status_code=status_code)

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
from fastapi.responses import JSONResponse
from fastapi import Body, HTTPException, Depends
from fastapi.routing import APIRouter
from typing import Any

from ..utils import success_response, prepare_dropdown_data
from .schema import RegisterEmployeeService, EmployeeServiceData, EmployeeServiceName
from ..queries import insert_item, prepare_item_list
from ..auth.helpers import JWTBearer

router = APIRouter()
employee_service_collection = 'employee_service'
service_collection = 'service'
employee_collection = 'employee'


@router.post("/v1/employee_service", response_description="Add new Employee Service")
def create_service(service: RegisterEmployeeService = Body(...), current_user: str = Depends(JWTBearer())) -> Any:
    """
    Register Service API
    """
    inserted_id = insert_item(employee_service_collection, service, current_user)
    response_data = success_response(data={'item_id': str(inserted_id)}, message="Successfully inserted data")
    return JSONResponse(content=response_data, status_code=201)


@router.get("/v1/employee_service", response_description="Get Service List", dependencies=[Depends(JWTBearer())])
def get_service(
        page_number: int = 1,
        page_size: int = 10,
        search_string: str = None
) -> Any:
    """
    Get Category List API
    """
    data_dict = {
        'collection_name': employee_service_collection,
        'schema': EmployeeServiceData,
        'page_number': page_number,
        'page_size': page_size,
        'search_string': search_string
    }
    response_data = prepare_item_list(data_dict)
    status_code = response_data.get("status")
    return JSONResponse(content=response_data, status_code=status_code)


@router.get("/v1/employee_list/{service_id}",
            response_description="Get Employee List",
            dependencies=[Depends(JWTBearer())])
def get_employee_list(
        service_id: str
) -> Any:
    """
    Get Category List API
    """
    employee_list_dict = {
        'collection_name': employee_collection,
        'schema': ['email', 'phone_number', 'country_code'],
    }
    employee_response = prepare_item_list(employee_list_dict)
    employee_dict = {employee['_id']: {**employee} for employee in employee_response.get('data', []) if employee}

    data_dict = {
        'collection_name': employee_service_collection,
        'schema': EmployeeServiceName,
        'filters': {'service_id': service_id}
    }
    response_data = prepare_item_list(data_dict)
    data = response_data.get("data", [])
    for emp in data:
        emp['employee'] = employee_dict.get(emp['employee_id'], {})

    response_data['data'] = data
    status_code = response_data.get("status")
    return JSONResponse(content=response_data, status_code=status_code)


@router.get("/v1/employee_service_dropdown_data",
            response_description="get service dropdown data",
            dependencies=[Depends(JWTBearer())])
async def user_dropdown():
    """
    get service dropdown data
    """
    data_list = prepare_dropdown_data(collection_name=employee_service_collection, label='name', value='_id')
    response_data = success_response(data=data_list, message="Successfully get data")
    status_code = response_data.get("status")
    return JSONResponse(content=response_data, status_code=status_code)




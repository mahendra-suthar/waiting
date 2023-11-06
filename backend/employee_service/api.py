from fastapi.responses import JSONResponse
from fastapi import Body, HTTPException
from fastapi.routing import APIRouter
from typing import Any

from ..utils import success_response, prepare_dropdown_data
from .schema import RegisterEmployeeService, EmployeeServiceData
from ..queries import insert_item, prepare_item_list

router = APIRouter()
employee_service_collection = 'employee_service'


@router.post("/v1/employee_service", response_description="Add new Employee Service")
def create_service(service: RegisterEmployeeService = Body(...)) -> Any:
    """
    Register Service API
    """
    inserted_id = insert_item(employee_service_collection, service)
    response_data = success_response(data={'item_id': str(inserted_id)}, message="Successfully inserted data")
    return JSONResponse(content=response_data, status_code=201)


@router.get("/v1/employee_service", response_description="Get Service List")
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


@router.get("/v1/employee_service_dropdown_data",
            response_description="get service dropdown data")
async def user_dropdown():
    """
    get service dropdown data
    """
    data_list = prepare_dropdown_data(collection_name=employee_service_collection, label='name', value='_id')
    response_data = success_response(data=data_list, message="Successfully get data")
    status_code = response_data.get("status")
    return JSONResponse(content=response_data, status_code=status_code)




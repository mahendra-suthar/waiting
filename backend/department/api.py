from fastapi.responses import JSONResponse
from fastapi import Body, HTTPException, Depends
from fastapi.routing import APIRouter
from typing import Any

from ..utils import success_response, prepare_dropdown_data
from .schema import RegisterDepartment
from ..queries import insert_item, prepare_item_list, get_item_list
from ..auth.helpers import JWTBearer

router = APIRouter()
department_collection = 'department'


@router.post("/v1/department", response_description="Add new Business Department")
def create_service(department: RegisterDepartment = Body(...), current_user: str = Depends(JWTBearer())) -> Any:
    """
    Register Department API
    """
    inserted_id = insert_item(department_collection, department, current_user)
    response_data = success_response(data={'item_id': str(inserted_id)}, message="Successfully inserted data")
    return JSONResponse(content=response_data, status_code=201)


# @router.get("/v1/service", response_description="Get Service List", dependencies=[Depends(JWTBearer())])
# def get_service(
#         page_number: int = 1,
#         page_size: int = 10,
#         search_string: str = None
# ) -> Any:
#     """
#     Get Service List API
#     """
#     data_dict = {
#         'collection_name': service_collection,
#         'schema': ServiceData,
#         'page_number': page_number,
#         'page_size': page_size,
#         'search_string': search_string
#     }
#     service_data = prepare_item_list(data_dict)
#     data_list = service_data.get('data', [])
#     business_data = get_item_list(collection_name=business_collection, columns=['name'])
#     business_data_list = business_data.get('data', [])
#     business_dict = {business['_id']: business['name'] for business in business_data_list if business}
#     for data in data_list:
#         data['business'] = business_dict[data['merchant_id']]
#
#     status_code = service_data.get("status")
#     service_data['data'] = data_list
#     return JSONResponse(content=service_data, status_code=status_code)
#
#
@router.get("/v1/department_dropdown_data",
            response_description="get department dropdown data",
            dependencies=[Depends(JWTBearer())])
async def department_dropdown(business_id: str = None):
    """
    get department dropdown data
    """
    data_list = prepare_dropdown_data(
        collection_name=department_collection,
        filters={'merchant_id': business_id},
        label='name', value='_id'
    )
    response_data = success_response(data=data_list, message="Successfully get data")
    status_code = response_data.get("status")
    return JSONResponse(content=response_data, status_code=status_code)




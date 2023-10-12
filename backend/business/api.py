from fastapi.routing import APIRouter
from fastapi import Body, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Any

from ..utils import success_response
from .schema import RegisterBusiness, UpdateBusiness, BusinessData
from .helpers import (insert_business_request, update_business_request, prepare_category_wise_business_list,
                      prepare_business_details_with_employee_queue)
from ..queries import prepare_item_list

router = APIRouter()
business_collection = 'business'


@router.post("/v1/business", response_description="Add new Business")
async def create_business(business: RegisterBusiness = Body(...)) -> Any:
    """
    Register business api
    """
    business_data = jsonable_encoder(business)
    inserted_business = await insert_business_request(business_data)
    response_data = success_response(data={'business_id': str(inserted_business)}, message="Successfully inserted data")
    return JSONResponse(content=response_data, status_code=201)


@router.put("/v1/business/{business_id}", response_description="Update Business")
async def update_business(business_id: str, business: UpdateBusiness = Body(...)) -> Any:
    """
    Update business details
    """
    business_data = jsonable_encoder(business)
    response_data = await update_business_request(business_id, business_data)
    status_code = response_data.get("status")
    return JSONResponse(content=response_data, status_code=status_code)


@router.get("/v1/business", response_description="Get Business")
def get_business(
        page_number: int = 1,
        page_size: int = 10,
        search_string: str = None
) -> Any:
    """
    Register business api
    """
    data_dict = {
        'collection_name': business_collection,
        'schema': BusinessData,
        'page_number': page_number,
        'page_size': page_size,
        'search_string': search_string
    }
    response_data = prepare_item_list(data_dict)
    status_code = response_data.get("status")
    return JSONResponse(content=response_data, status_code=status_code)


@router.get("/v1/category_business_list", response_description="Get Business")
def get_category_wise_business_list() -> Any:
    """
    Get category wise business api
    """
    response_data = prepare_category_wise_business_list()
    status_code = response_data.get("status")
    return JSONResponse(content=response_data, status_code=status_code)


@router.get("/v1/business_employee_waiting/{business_id}", response_description="Get Business")
def get_category_wise_business_list(business_id: str) -> Any:
    """
    Get category wise business api
    """
    data_dict = {
        'business_id': business_id
    }
    response_data = prepare_business_details_with_employee_queue(data_dict)
    status_code = response_data.get("status")
    return JSONResponse(content=response_data, status_code=status_code)

from fastapi.routing import APIRouter
from fastapi import Body, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Any

from ..utils import success_response
from .schema import RegisterBusiness, UpdateBusiness, BusinessData
from .helpers import (insert_business_request, update_business_request, prepare_category_wise_business_list,
                      prepare_business_details_with_employee_queue)
from ..queries import prepare_item_list, get_item, get_item_list
from ..auth.helpers import JWTBearer
from ..constants import days_of_week_choices

router = APIRouter()
business_collection = 'business'
category_collection = 'category'
business_schedule_collection = 'business_schedule'


@router.post("/v1/business", response_description="Add new Business")
async def create_business(business: RegisterBusiness = Body(...), current_user: str = Depends(JWTBearer())) -> Any:
    """
    Register business api
    """
    business_data = jsonable_encoder(business)
    business_data['created_by'] = current_user
    inserted_business = await insert_business_request(business_data)
    response_data = success_response(data={'business_id': str(inserted_business)}, message="Successfully inserted data")
    return JSONResponse(content=response_data, status_code=201)


@router.put("/v1/business/{business_id}", response_description="Update Business")
async def update_business(
        business_id: str, business: UpdateBusiness = Body(...),
        current_user: str = Depends(JWTBearer())) -> Any:
    """
    Update business details
    """
    business_data = jsonable_encoder(business)
    business_data['updated_by'] = current_user
    response_data = await update_business_request(business_id, business_data)
    status_code = response_data.get("status")
    return JSONResponse(content=response_data, status_code=status_code)


@router.get("/v1/business", response_description="Get Business", dependencies=[Depends(JWTBearer())])
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


@router.get("/v1/category_business_list", response_description="Get Business", dependencies=[Depends(JWTBearer())])
def get_category_wise_business_list() -> Any:
    """
    Get category wise business api
    """
    response_data = prepare_category_wise_business_list()
    status_code = response_data.get("status")
    return JSONResponse(content=response_data, status_code=status_code)


@router.get("/v1/business_employee_waiting/{business_id}",
            response_description="Get Business",
            dependencies=[Depends(JWTBearer())])
def get_category_wise_business_list(business_id: str) -> Any:
    """
    Get business with employee queue count
    """
    data_dict = {
        'business_id': business_id
    }
    response_data = prepare_business_details_with_employee_queue(data_dict)
    status_code = response_data.get("status")
    return JSONResponse(content=response_data, status_code=status_code)


@router.get("/v1/business/{business_id}", response_description="Get Business", dependencies=[Depends(JWTBearer())])
def get_business_details(business_id: str) -> Any:
    """
    Get business details
    """
    response_data = get_item(
        collection_name=business_collection,
        item_id=business_id,
        columns=['name', 'email', 'country_code', 'phone_number', 'status', 'category_id', 'owner_id', 'about_business']
    )
    status_code = response_data.get("status")
    data = response_data.get("data")
    category_id = data.get("category_id")
    business_schedule = get_item_list(
        collection_name=business_schedule_collection,
        columns=['day_of_week', 'opening_time', 'closing_time']
    )
    week_day_dict = dict(days_of_week_choices)
    business_schedule = business_schedule.get('data', [])
    business_schedule = [
        {**business, 'day_of_week': week_day_dict.get(business.get('day_of_week'))} for business in business_schedule
        if business
    ]
    data['business_schedule'] = business_schedule
    if category_id:
        category_data = get_item(
            collection_name=category_collection,
            item_id=category_id,
            columns=['name', 'description']
        )
        data['category_details'] = category_data.get("data")
    return JSONResponse(content=response_data, status_code=status_code)




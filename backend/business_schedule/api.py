from fastapi.routing import APIRouter
from fastapi import Body, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Any
#
from ..utils import success_response
from .schema import RegisterBusinessSchedule, BusinessScheduleData
# from .helpers import (insert_business_request, update_business_request, prepare_category_wise_business_list,
#                       prepare_business_details_with_employee_queue)
from ..queries import prepare_item_list, get_item

router = APIRouter()
business_schedule_collection = 'business_schedule'


@router.get("/v1/business_schedule/{business_id}", response_description="Get Business Schedules")
def get_business_schedule(business_id: str) -> Any:
    """
    Get Business Schedules api
    """
    data_dict = {
        'collection_name': business_schedule_collection,
        'schema': BusinessScheduleData,
        'filters': {'merchant_id': business_id}
    }
    response_data = prepare_item_list(data_dict)
    data = response_data.get("data")
    response_data['data'] = sorted(data, key=lambda x: x.get('day_of_week', 0), reverse=True)
    return JSONResponse(content=response_data, status_code=response_data.get("status"))
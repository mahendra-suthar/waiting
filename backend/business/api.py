from fastapi.routing import APIRouter
from fastapi import Body, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Any

from ..utils import success_response
from .schema import RegisterBusiness, UpdateBusiness
from .helpers import insert_business_request, update_business_request

router = APIRouter()


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

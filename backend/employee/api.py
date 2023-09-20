from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import Body, HTTPException
from fastapi.routing import APIRouter
from typing import Any

from ..utils import success_response
from .schema import RegisterEmployee
from .helpers import insert_employee_request


router = APIRouter()


@router.post("/v1/employee", response_description="Add new Employee")
async def create_employee(employee: RegisterEmployee = Body(...)) -> Any:
    """
    Register employee api
    """
    employee_data = jsonable_encoder(employee)
    inserted_employee = await insert_employee_request(employee_data)
    response_data = success_response(data={'employee_id': str(inserted_employee)}, message="Successfully inserted data")
    return JSONResponse(content=response_data, status_code=201)

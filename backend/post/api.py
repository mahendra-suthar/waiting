from fastapi.responses import JSONResponse
from fastapi import Body, HTTPException
from fastapi.routing import APIRouter
from typing import Any

from ..utils import success_response, prepare_dropdown_data
from .schema import RegisterPost, PostData
from ..queries import insert_item, prepare_item_list

router = APIRouter()
post_collection = 'post'


@router.post("/v1/post", response_description="Post")
def create_post(post: RegisterPost = Body(...)) -> Any:
    """
    Register Business Post API
    """
    inserted_id = insert_item(post_collection, post)
    response_data = success_response(data={'item_id': str(inserted_id)}, message="Successfully inserted data")
    return JSONResponse(content=response_data, status_code=201)


@router.get("/v1/post", response_description="Get post List")
def get_service(
        page_number: int = 1,
        page_size: int = 10,
        search_string: str = None
) -> Any:
    """
    Get Post List API
    """
    data_dict = {
        'collection_name': post_collection,
        'schema': PostData,
        'page_number': page_number,
        'page_size': page_size,
        'search_string': search_string
    }
    response_data = prepare_item_list(data_dict)
    status_code = response_data.get("status")
    return JSONResponse(content=response_data, status_code=status_code)

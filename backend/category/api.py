from fastapi.responses import JSONResponse
from fastapi import Body, HTTPException, Depends, status
from fastapi.routing import APIRouter
from typing import Any

from ..utils import success_response
from .schema import RegisterCategory, CategoryData
from ..queries import insert_item, prepare_item_list, filter_data
from ..auth.helpers import JWTBearer

router = APIRouter()
category_collection = 'category'


@router.post("/v1/category", response_description="Add new Category")
def create_category(category: RegisterCategory = Body(...), current_user: str = Depends(JWTBearer())) -> Any:
    """
    Register Category API
    """
    name_exist = filter_data(
        collection_name=category_collection,
        filter_dict={'name': category.name}
    )
    if name_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category Name already exist")

    parent_category_id = category.parent_category_id
    if parent_category_id:
        parent_category_exist = filter_data(
            collection_name=category_collection,
            filter_dict={'_id': parent_category_id}
        )
        if not parent_category_exist:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category Id not exist")
    inserted_id = insert_item(category_collection, category, current_user)
    response_data = success_response(data={'item_id': str(inserted_id)}, message="Successfully inserted data")
    return JSONResponse(content=response_data, status_code=201)


@router.get("/v1/category", response_description="Get Category List", dependencies=[Depends(JWTBearer())])
def get_category(
        page_number: int = 1,
        page_size: int = 10,
        search_string: str = None
) -> Any:
    """
    Get Category List API
    """
    data_dict = {
        'collection_name': category_collection,
        'schema': CategoryData,
        'page_number': page_number,
        'page_size': page_size,
        'search_string': search_string
    }
    response_data = prepare_item_list(data_dict)
    status_code = response_data.get("status")
    return JSONResponse(content=response_data, status_code=status_code)

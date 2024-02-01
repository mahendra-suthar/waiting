import os
from fastapi import UploadFile

from .schema import RegisterPost, PostData
from ..queries import prepare_item_list
from ..utils import get_current_timestamp_utc

post_collection = 'post'


def jinja_variables_for_post_service():
    data_dict = {
        'collection_name': post_collection,
        'schema': RegisterPost
    }
    columns = list(PostData.__annotations__.keys())
    data = prepare_item_list(data_dict)
    table_name = post_collection
    name = 'Post'
    return columns, data, name, table_name


async def save_uploaded_file(file: UploadFile) -> str:
    file_name = f"post_{get_current_timestamp_utc()}"
    _, extension = os.path.splitext(file.filename)
    new_filename = f"{file_name}{extension}"
    file_path = f"/business-post/{new_filename}"  # Update the path as needed
    with open(f"/app/{file_path}", "wb") as f:
        f.write(file.file.read())
    return file_path
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles

from backend.users.api import router as user_router
from backend.business.api import router as business_router
from backend.auth.api import router as auth_router
from backend.employee.api import router as employee_router
from backend.category.api import router as category_router
# from backend.queue.api import router as queue_router
from backend.queue_user.api import router as queue_user_router
from backend.employee_service.api import router as employee_service_router
from backend.service.api import router as service_router
from backend.websocket import router as websocket_router

from backend.users.web import router as user_web_router
from backend.employee.web import router as employee_web_router
from backend.business.web import router as business_web_router
from backend.category.web import router as category_web_router
from backend.queue.web import router as queue_web_router
from backend.queue_user.web import router as queue_user_web_router
from backend.service.web import router as service_web_router
from backend.business_schedule.web import router as business_schedule_web_router
from backend.employee_service.web import router as employee_service_web_router

from backend.utils import error_response

import sys
sys.path.append("E:/projects/test/waiting/")

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to waiting"}

app.mount("/static", StaticFiles(directory=r"static"), name="static")


app.include_router(user_router, prefix="/api", tags=['USER'])
app.include_router(business_router, prefix="/api", tags=['BUSINESS'])
app.include_router(employee_router, prefix="/api", tags=['EMPLOYEE'])
app.include_router(auth_router, prefix="/api", tags=['AUTH'])
app.include_router(category_router, prefix="/api", tags=['CATEGORY'])
app.include_router(category_router, prefix="/api", tags=['CATEGORY'])
app.include_router(queue_user_router, prefix="/api", tags=['QUEUE_USER'])
app.include_router(employee_service_router, prefix="/api", tags=['EMPLOYEE_SERVICE'])
app.include_router(service_router, prefix="/api", tags=['SERVICE'])
app.include_router(websocket_router, prefix="", tags=['WEBSOCKET'])

app.include_router(user_web_router, prefix="/web", tags=['USER'])
app.include_router(employee_web_router, prefix="/web", tags=['EMPLOYEE'])
app.include_router(business_web_router, prefix="/web", tags=['BUSINESS'])
app.include_router(category_web_router, prefix="/web", tags=['CATEGORY'])
app.include_router(queue_web_router, prefix="/web", tags=['QUEUE'])
app.include_router(queue_user_web_router, prefix="/web", tags=['QUEUE_USER'])
app.include_router(service_web_router, prefix="/web", tags=['SERVICE'])
app.include_router(business_schedule_web_router, prefix="/web", tags=['BUSINESS_SCHEDULE'])
app.include_router(employee_service_web_router, prefix="/web", tags=['EMPLOYEE_SERVICE'])

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    error_content = error_response(error=exc.detail)
    return JSONResponse(content=error_content, status_code=exc.status_code)


# Custom error handler for RequestValidationError
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_messages = []
    for error in exc.errors():
        field_name = error["loc"][1]
        error_message = {'field': field_name, 'error': error['msg'], 'type': error['type']}
        error_messages.append(error_message)
    error_content = error_response(error=error_messages)
    return JSONResponse(content=error_content, status_code=422)

if __name__ == "__main__":
    print("Running...")
#     uvicorn.run(app, host="127.0.0.1", port=8000)

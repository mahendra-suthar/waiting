from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from backend.users.api import router as user_router
from backend.auth.api import router as auth_router
from backend.utils import error_response

app = FastAPI()


app.include_router(user_router, prefix="/api", tags=['USER'])
app.include_router(auth_router, prefix="/api", tags=['AUTH'])


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    print("--------exc-------", exc.detail)
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
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(8001))
#     uvicorn.run(app, host="127.0.0.1", port=8000)

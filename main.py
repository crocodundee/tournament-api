import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from api.users import router as users_router

app = FastAPI()
app.include_router(users_router, prefix="/users")


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Returns unified validation responses with 400 status."""
    errors = [
        {"loc": error["loc"], "msg": error["msg"], "type": error["type"]}
        for error in exc.errors()
    ]
    return JSONResponse(
        content={"detail": jsonable_encoder(errors)},
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@app.get("/")
def healthcheck():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

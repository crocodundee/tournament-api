import uvicorn
from fastapi import FastAPI

from api.users import router as users_router

app = FastAPI()
app.include_router(users_router, prefix="/users")


@app.get("/")
async def healthcheck():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

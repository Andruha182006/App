from fastapi import FastAPI
from api.v1.router import router

app = FastAPI()

app.include_router(router)

app = FastAPI(
    title="My FastAPI Project",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json"
)
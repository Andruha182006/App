from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from api.v1.router import router
from core.middleware import TimingAndLoggingMiddleware


app = FastAPI(
    title="My FastAPI Project",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json"
)

app.add_middleware(TimingAndLoggingMiddleware)

app.include_router(router)


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    """Перетворює порушення unique/FK-обмежень на зрозумілу відповідь 409."""
    return JSONResponse(
        status_code=409,
        content={"detail": "Resource conflicts with existing data or references missing records"},
    )

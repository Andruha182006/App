import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import DataError, IntegrityError

from api.v1.router import router
from core.config import settings
from core.middleware import TimingAndLoggingMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="StudyFlow",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
)

app.add_middleware(TimingAndLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Process-Time"],
)

app.include_router(router)


@app.get("/", tags=["System"])
async def root() -> dict[str, str]:
    return {
        "name": app.title,
        "version": app.version,
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", tags=["System"])
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.exception_handler(DataError)
async def data_error_handler(request: Request, exc: DataError) -> JSONResponse:
    """Перетворює занадто довгі або некоректні значення на 422."""
    logger.warning(
        "DataError on %s %s: %s",
        request.method,
        request.url.path,
        exc.orig,
    )
    return JSONResponse(
        status_code=422,
        content={"detail": "Value is too long or has invalid format"},
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(
    request: Request,
    exc: IntegrityError,
) -> JSONResponse:
    """Перетворює порушення обмежень БД на зрозумілу відповідь 409."""
    sqlstate = getattr(exc.orig, "sqlstate", None) or getattr(
        exc.orig, "pgcode", None
    )

    if sqlstate == "23505":
        detail = "Resource with these unique fields already exists"
    elif sqlstate == "23503":
        if request.method == "DELETE":
            detail = "Cannot delete: record is referenced by other data"
        else:
            detail = "Referenced record does not exist"
    elif sqlstate == "23502":
        detail = "Required field is missing"
    else:
        detail = "Resource conflicts with existing data"

    logger.warning(
        "IntegrityError on %s %s: %s",
        request.method,
        request.url.path,
        exc.orig,
    )
    return JSONResponse(status_code=409, content={"detail": detail})

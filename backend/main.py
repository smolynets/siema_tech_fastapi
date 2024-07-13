import datetime
import logging
from logging.config import dictConfig

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware

from backend import config
from backend.items.router import router as items_router
from backend.logger import LogConfig

dictConfig(LogConfig().model_dump())

logger = logging.getLogger(f"{config.SERVICE_NAME}_logger")


app = FastAPI(
    title=f"{config.SERVICE_NAME} API",
    description=f"API for the {config.SERVICE_NAME} project",
    version="0.0.1",
    contact={},
    openapi_url=config.OPENAPI_URL if config.DEBUG else None,
    docs_url=config.DOCS_URL if config.DEBUG else None,
    redoc_url=config.REDOC_URL if config.DEBUG else None,
    debug=config.DEBUG
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse({"detail": [{"msg": exc.detail, "loc": [], "type": "error"}]}, status_code=exc.status_code)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True if config.DEBUG else False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


app.include_router(items_router, prefix="/api/v1/items", tags=["items"])

@app.on_event("startup")
async def startup_event():
   logger.debug('Server started')
   
@app.on_event("shutdown")
async def shutdown_event():
   logger.debug('Server shutdown')
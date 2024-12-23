from loguru import logger
from authx import AuthX, AuthXConfig
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from contextlib import asynccontextmanager

from app.database.db import init_db
from app.middlewares import log_middle
from app.config import (
    REDOC_URL,
    DOCS_URL,
    ORIGINS,
    HOST,
    PORT,
    DEBUG,
    JWT_PRIVATE_KEY_PATH,
    JWT_PUBLIC_KEY_PATH,
    JWT_ALGORITHM,
    ACCESS_TOKEN_EXPIRES_MINUTES,
)
from app.routers import blog, auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    await init_db()
    authx_config = AuthXConfig()
    authx_config.JWT_SECRET_KEY = JWT_PRIVATE_KEY_PATH.read_text().strip()
    authx_config.JWT_PUBLIC_KEY = JWT_PUBLIC_KEY_PATH.read_text().strip()
    authx_config.JWT_ALGORITHM = JWT_ALGORITHM
    authx_config.JWT_ACCESS_COOKIE_NAME = "access_token"
    authx_config.JWT_TOKEN_LOCATION = ["cookies", "headers"]
    authx_config.JWT_ACCESS_TOKEN_EXPIRES = ACCESS_TOKEN_EXPIRES_MINUTES
    authx_config.JWT_COOKIE_CSRF_PROTECT = False
    authx_config.JWT_CSRF_IN_COOKIES = False

    app.state.security = AuthX(authx_config)

    try:
        yield
    finally:
        logger.info("Shutting down...")


app = FastAPI(lifespan=lifespan, docs_url=DOCS_URL, redoc_url=REDOC_URL)

# Add the middleware to the app
app.add_middleware(BaseHTTPMiddleware, dispatch=log_middle)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(blog.router)
app.include_router(auth.router)

if __name__ == "__main__":
    from uvicorn_loguru_integration import run_uvicorn_loguru
    import uvicorn

    run_uvicorn_loguru(
        uvicorn.Config(
            "app.main:app", host=HOST, port=PORT, reload=DEBUG, log_level="debug"
        )
    )

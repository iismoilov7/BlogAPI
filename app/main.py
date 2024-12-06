from loguru import logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.middlewares import log_middle
from  contextlib import asynccontextmanager
from app.config import (
    REDOC_URL,
    DOCS_URL,
    ORIGINS,
    HOST,
    PORT,
    DEBUG
)
from app.routers import blog

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
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

if __name__ == "__main__":
    from uvicorn_loguru_integration import run_uvicorn_loguru
    import uvicorn
    
    run_uvicorn_loguru(
        uvicorn.Config(
            "app.main:app",
            host=HOST,
            port=PORT,
            reload=DEBUG,
            log_level="debug"
        )
    )

import sys
from loguru import logger
from starlette.routing import Match
from fastapi import Request

logger.remove()
# Add a logger that writes to a file
logger.add("requests.log", enqueue=True, rotation="1 week")  # You can specify rotation if needed
# Add a logger that writes to stdout with colorization
logger.add(sys.stdout, colorize=True)

async def log_middle(request: Request, call_next):
    logger.debug(f"{request.method} {request.url}")
    routes = request.app.router.routes
    logger.debug("Params:")
    for route in routes:
        match, scope = route.matches(request)
        if match == Match.FULL:
            for name, value in scope["path_params"].items():
                logger.debug(f"\t{name}: {value}")
    logger.debug("Headers:")
    for name, value in request.headers.items():
        logger.debug(f"\t{name}: {value}")

    response = await call_next(request)
    return response

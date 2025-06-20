import logging
import time
from fastapi import FastAPI, Request

def setup_logging(app: FastAPI):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    if not logger.hasHandlers():
        stream_handler = logging.StreamHandler()
        file_handler = logging.FileHandler("wall_robot.log")
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        stream_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        logger.info(f"Incoming request: {request.method} {request.url}")
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        logger.info(f"Completed request: {request.method} {request.url} in {duration:.4f} seconds")
        return response

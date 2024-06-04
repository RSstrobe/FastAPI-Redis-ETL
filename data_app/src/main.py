import logging

import uvicorn

from app import create_app
from core.config import settings
from core.logger import LOGGING

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.backend.backend_host,
        port=settings.backend.backend_port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )

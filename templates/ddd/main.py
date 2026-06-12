from fastapi import FastAPI

from app.config.lifespan import lifespan
from app.config.settings import get_settings
from app.presentation.router.api_router import api_router
from app.shared.exceptions.handlers import register_exception_handlers
from app.shared.logging.logger import get_logger, setup_logging

logger = get_logger(__name__)


def create_app() -> FastAPI:
    settings = get_settings()
    setup_logging(settings.logging.log_level)

    app = FastAPI(title=settings.app.app_name, debug=settings.app.debug, lifespan=lifespan)

    register_exception_handlers(app)
    app.include_router(api_router)
    logger.info("Application created: %s", settings.app.app_name)
    return app


app = create_app()

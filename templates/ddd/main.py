from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.lifespan import lifespan
from app.config.settings import get_settings
from app.presentation.router.api_router import api_router
from app.shared.exceptions.handlers import register_exception_handlers
from app.shared.logging.logger import get_logger, setup_logging
from app.shared.middleware.timing import ProcessTimeMiddleware

logger = get_logger(__name__)


def create_app() -> FastAPI:
    settings = get_settings()
    setup_logging(settings.logging.log_level)

    # Not wired to settings.app.debug: Starlette's debug mode renders raw
    # tracebacks for unhandled exceptions, bypassing register_exception_handlers
    # below and breaking the uniform ApiResponse error envelope this project
    # relies on (see AGENTS.md/CLAUDE.md "API 응답과 에러").
    app = FastAPI(title=settings.app.app_name, lifespan=lifespan)

    if settings.cors.is_active:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors.allow_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        logger.info("CORS enabled for %s", settings.cors.allow_origins)

    app.add_middleware(ProcessTimeMiddleware)
    register_exception_handlers(app)
    app.include_router(api_router)
    logger.info("Application created: %s", settings.app.app_name)
    return app


app = create_app()

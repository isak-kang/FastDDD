from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.shared.logging.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("Application startup")
    await _startup(app)

    try:
        yield
    finally:
        await _shutdown(app)
        logger.info("Application shutdown")


async def _startup(app: FastAPI) -> None:
    # Wire external resources here. See AGENTS.md and .cursor/skills/add-lifespan-resource/.
    # 1. get_settings() and create clients under app/infrastructure/
    # 2. attach clients to app.state (e.g. app.state.redis)
    # 3. set app.state.ready = True only after required resources succeed
    app.state.ready = True


async def _shutdown(app: FastAPI) -> None:
    # Close clients in reverse startup order. See add-lifespan-resource skill.
    app.state.ready = False

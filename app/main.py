import logging

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.database import Base, engine
import app.models  # noqa: F401 — registers all models with SQLAlchemy before create_all
from app.routers import auth, favourites, locations, operators, tickets, travel_log, zones

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auto-create tables on startup.
# For production, replace with Alembic migrations: `alembic upgrade head`
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(locations.router)
app.include_router(operators.router)
app.include_router(tickets.router)
app.include_router(zones.router)
app.include_router(favourites.router)
app.include_router(travel_log.router)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled server error on %s: %s", request.url, exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "An unexpected error occurred. Please try again later.",
        },
    )


@app.get("/health", tags=["health"])
def health_check() -> dict:
    return {"status": "ok"}

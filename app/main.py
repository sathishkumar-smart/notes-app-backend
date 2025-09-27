# app/main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from dotenv import load_dotenv
import logging
import time

from app.core.config import settings
from app.core.logging import setup_logging
from app.routers import auth, notes

# ------------------------------------------------------------------------------
# Load environment variables early
# ------------------------------------------------------------------------------
load_dotenv()

# ------------------------------------------------------------------------------
# Configure centralized logging
# ------------------------------------------------------------------------------
setup_logging()
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------
# Initialize FastAPI application
# ------------------------------------------------------------------------------
app = FastAPI(
    title="Notes App API",
    description="Backend service for Notes App. Provides authentication and "
                "note management APIs with JWT-based security.",
    version="1.0.0",
)


# ------------------------------------------------------------------------------
# Middleware: CORS
# ------------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------------------------------------------------------------
# Middleware: Request/Response Logging
# Logs request method, path, and execution time for observability
# ------------------------------------------------------------------------------
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = round(time.time() - start_time, 4)

        logger.info(
            f"{request.method} {request.url.path} "
            f"completed_in={duration}s status={response.status_code}"
        )
        return response


app.add_middleware(LoggingMiddleware)


# ------------------------------------------------------------------------------
# Exception Handlers
# ------------------------------------------------------------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Catch-all exception handler for unexpected errors.
    Ensures client gets a consistent response format.
    """
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error. Please try again later."},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handles request validation errors from Pydantic models.
    Returns human-readable messages instead of raw traceback.
    """
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )


# ------------------------------------------------------------------------------
# Routers (Feature Modules)
# ------------------------------------------------------------------------------
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(notes.router, prefix="/api/notes", tags=["Notes"])


# ------------------------------------------------------------------------------
# Health Check Route
# Used by monitoring tools (K8s, Docker, uptime checks) to verify service health
# ------------------------------------------------------------------------------
@app.get("/api/health", tags=["Health"])
async def health_check():
    """
    Simple health check endpoint.
    Returns 200 OK if service is running.
    """
    return {"status": "ok", "service": "Notes App API"}


# ------------------------------------------------------------------------------
# Lifecycle Events
# ------------------------------------------------------------------------------
@app.on_event("startup")
async def startup_event():
    """
    Runs at application startup.
    Ideal for:
      - DB connection warm-up
      - Preloading configuration
      - Scheduling background jobs
    """
    logger.info("Application startup: Notes App API is running.")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Runs at application shutdown.
    Ideal for:
      - Closing DB connections
      - Flushing caches
      - Stopping background workers
    """
    logger.info("Application shutdown: Cleaning up resources...")

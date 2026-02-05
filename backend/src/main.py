from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from .api.routes.chat import router as chat_router
from .api.auth_router import router as auth_router
from .api.todo_router import router as todo_router
from .api.task_router import router as task_router
from .core.database import init_db
from .models import *  # Import all models to register them with SQLModel
from .core.config import settings
import logging
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized successfully!")
    yield
    # Shutdown

app = FastAPI(
    title=settings.app_name,
    description="API for agent-orchestrated task management via MCP tools",
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
# Replace the existing chat endpoint with our stateless version
from .api.routes.chat import router as stateless_chat_router
app.include_router(stateless_chat_router, prefix="/api/v1", tags=["chat"])

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(todo_router, prefix="/api/todos", tags=["todos"])
app.include_router(task_router, prefix="/api", tags=["tasks"])

# Include our new health check endpoints
from .api.routes.health import router as health_router
app.include_router(health_router, prefix="/api/v1", tags=["health"])

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"detail": jsonable_encoder(exc.errors())},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"General error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": settings.app_name, "version": settings.app_version}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "agent-task-management-api", "version": settings.app_version}
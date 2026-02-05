"""Health check endpoints for the stateless conversation cycle."""

from fastapi import APIRouter
from typing import Dict
from datetime import datetime


router = APIRouter(tags=["health"])


@router.get("/health")
async def overall_health() -> Dict[str, str]:
    """Overall health check for the API."""
    return {
        "status": "healthy",
        "service": "stateless-chat-api",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/ready")
async def readiness_check() -> Dict[str, str]:
    """Readiness check for the API."""
    # Here we would check if all dependencies are ready
    # For now, we'll just return healthy
    return {
        "status": "ready",
        "service": "stateless-chat-api",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/live")
async def liveness_check() -> Dict[str, str]:
    """Liveness check for the API."""
    return {
        "status": "alive",
        "service": "stateless-chat-api",
        "timestamp": datetime.utcnow().isoformat()
    }
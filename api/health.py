"""
Health check and monitoring endpoints for AI-Researcher
"""

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Optional
import os
import psutil
import time
from datetime import datetime

app = FastAPI(
    title="AI-Researcher Health API",
    description="Health check and monitoring endpoints",
    version="0.2.0"
)

# Global startup time
STARTUP_TIME = time.time()

class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    version: str
    uptime_seconds: float
    timestamp: str
    checks: Dict[str, bool]
    details: Optional[Dict] = None

class ReadinessResponse(BaseModel):
    """Readiness check response model"""
    ready: bool
    services: Dict[str, bool]
    message: Optional[str] = None

@app.get("/health", response_model=HealthResponse, tags=["Monitoring"])
async def health_check():
    """
    Basic health check endpoint

    Returns:
        HealthResponse: Current health status
    """
    checks = {
        "api": True,
        "memory": psutil.virtual_memory().percent < 90,
        "disk": psutil.disk_usage('/').percent < 90,
        "cpu": psutil.cpu_percent(interval=0.1) < 95,
    }

    # Check environment variables
    required_env_vars = ["COMPLETION_MODEL", "CATEGORY"]
    checks["environment"] = all(os.getenv(var) for var in required_env_vars)

    all_healthy = all(checks.values())
    status_code = status.HTTP_200_OK if all_healthy else status.HTTP_503_SERVICE_UNAVAILABLE

    uptime = time.time() - STARTUP_TIME

    response = {
        "status": "healthy" if all_healthy else "unhealthy",
        "version": "0.2.0",
        "uptime_seconds": round(uptime, 2),
        "timestamp": datetime.utcnow().isoformat(),
        "checks": checks,
        "details": {
            "memory_percent": round(psutil.virtual_memory().percent, 2),
            "memory_available_gb": round(psutil.virtual_memory().available / (1024**3), 2),
            "disk_percent": round(psutil.disk_usage('/').percent, 2),
            "disk_free_gb": round(psutil.disk_usage('/').free / (1024**3), 2),
            "cpu_percent": round(psutil.cpu_percent(interval=0.1), 2),
            "cpu_count": psutil.cpu_count(),
        }
    }

    return JSONResponse(status_code=status_code, content=response)

@app.get("/ready", response_model=ReadinessResponse, tags=["Monitoring"])
async def readiness_check():
    """
    Readiness check endpoint (Kubernetes style)

    Returns:
        ReadinessResponse: Service readiness status
    """
    services = {}

    # Check critical environment variables
    services["env_vars"] = all([
        os.getenv("COMPLETION_MODEL"),
        os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
    ])

    # Check filesystem
    services["filesystem"] = os.path.exists("/workplace") and os.access("/workplace", os.W_OK)

    # Check if cache directory is writable
    cache_path = os.getenv("CACHE_PATH", "cache")
    services["cache"] = os.path.exists(cache_path) and os.access(cache_path, os.W_OK)

    # Check system resources
    services["resources"] = (
        psutil.virtual_memory().percent < 95 and
        psutil.disk_usage('/').percent < 95
    )

    ready = all(services.values())

    message = None
    if not ready:
        failed_services = [k for k, v in services.items() if not v]
        message = f"Not ready: {', '.join(failed_services)}"

    status_code = status.HTTP_200_OK if ready else status.HTTP_503_SERVICE_UNAVAILABLE

    response = {
        "ready": ready,
        "services": services,
        "message": message
    }

    return JSONResponse(status_code=status_code, content=response)

@app.get("/", tags=["Info"])
async def root():
    """
    Root endpoint with API information
    """
    return {
        "name": "AI-Researcher",
        "version": "0.2.0",
        "description": "Autonomous Scientific Innovation Platform",
        "endpoints": {
            "health": "/health",
            "ready": "/ready",
            "docs": "/docs"
        },
        "github": "https://github.com/HKUDS/AI-Researcher"
    }

@app.get("/ping", tags=["Monitoring"])
async def ping():
    """
    Simple ping endpoint
    """
    return {"status": "pong", "timestamp": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

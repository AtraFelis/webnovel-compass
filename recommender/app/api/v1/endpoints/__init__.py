"""
API v1 엔드포인트 모듈
"""

from .recommendations import router as recommendations_router
from .health import router as health_router

__all__ = [
    "recommendations_router",
    "health_router"
]

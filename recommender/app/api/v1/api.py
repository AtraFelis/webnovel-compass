"""
API v1 라우터 통합
"""
from fastapi import APIRouter

from app.api.v1.endpoints import recommendations_router, health_router
from app.api.v1.endpoints.test import router as test_router

api_router = APIRouter()

# 각 엔드포인트 라우터 등록
api_router.include_router(
    recommendations_router,
    tags=["추천"]
)

api_router.include_router(
    health_router,
    prefix="/health", 
    tags=["헬스체크"]
)

api_router.include_router(
    test_router,
    prefix="/test",
    tags=["테스트"]
)

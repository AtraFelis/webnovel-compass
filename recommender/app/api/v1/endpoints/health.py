"""
헬스체크 API 엔드포인트
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from datetime import datetime

from app.core.clients import health_check_clients
from app.config import settings
import structlog

logger = structlog.get_logger(__name__)

router = APIRouter()


@router.get(
    "",
    summary="서비스 상태 확인",
    description="추천 서비스와 연결된 모든 외부 서비스의 상태를 확인합니다."
)
async def health_check() -> Dict[str, Any]:
    """
    헬스체크 API
    
    추천 서비스의 전체적인 상태와 의존 서비스들의 연결 상태를 확인합니다.
    """
    try:
        # 외부 서비스 상태 확인
        client_health = await health_check_clients()
        
        # 전체 상태 판단
        all_healthy = all(client_health.values())
        
        response = {
            "status": "healthy" if all_healthy else "degraded",
            "timestamp": datetime.now().isoformat(),
            "service": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "dependencies": {
                "spring_boot": {
                    "status": "healthy" if client_health.get("spring_boot", False) else "unhealthy",
                    "description": "Spring Boot 백엔드 API"
                },
                "redis": {
                    "status": "healthy" if client_health.get("redis", False) else "unhealthy", 
                    "description": "Redis 캐시 서버"
                }
            }
        }
        
        if all_healthy:
            logger.info("헬스체크 통과", status="healthy")
        else:
            logger.warning("헬스체크 실패", status="degraded", dependencies=client_health)
            
        return response
        
    except Exception as e:
        logger.error("헬스체크 오류", error=str(e))
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "error": "헬스체크 실행 중 오류가 발생했습니다.",
                "timestamp": datetime.now().isoformat()
            }
        )


@router.get(
    "/simple",
    summary="간단한 상태 확인",
    description="추천 서비스의 기본적인 응답 여부만 확인합니다."
)
async def simple_health_check() -> Dict[str, str]:
    """
    간단한 헬스체크 API
    
    로드밸런서나 모니터링 시스템에서 사용할 수 있는 간단한 상태 확인입니다.
    """
    return {
        "status": "ok",
        "service": "webnovel-recommender",
        "timestamp": datetime.now().isoformat()
    }

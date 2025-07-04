"""
클라이언트 팩토리 및 의존성 관리
"""
from typing import Optional
from .spring_client import SpringBootClient
from .redis_client import RedisClient
import structlog

logger = structlog.get_logger(__name__)

# 전역 클라이언트 인스턴스
_spring_client: Optional[SpringBootClient] = None
_redis_client: Optional[RedisClient] = None


async def get_spring_client() -> SpringBootClient:
    """Spring Boot 클라이언트 인스턴스 반환"""
    global _spring_client
    if _spring_client is None:
        _spring_client = SpringBootClient()
        logger.info("Spring Boot 클라이언트 생성")
    return _spring_client


async def get_redis_client() -> RedisClient:
    """Redis 클라이언트 인스턴스 반환"""
    global _redis_client
    if _redis_client is None:
        _redis_client = RedisClient()
        await _redis_client.connect()
        logger.info("Redis 클라이언트 생성 및 연결")
    return _redis_client


async def close_clients():
    """모든 클라이언트 연결 종료"""
    global _spring_client, _redis_client
    
    if _spring_client:
        await _spring_client.close()
        _spring_client = None
        logger.info("Spring Boot 클라이언트 종료")
    
    if _redis_client:
        await _redis_client.close()
        _redis_client = None
        logger.info("Redis 클라이언트 종료")


async def health_check_clients() -> dict:
    """모든 클라이언트 상태 확인"""
    health_status = {
        "spring_boot": False,
        "redis": False
    }
    
    try:
        # Spring Boot 상태 확인 (간단한 요청으로 테스트)
        spring_client = await get_spring_client()
        # TODO: 실제로는 health check 엔드포인트를 호출해야 함
        health_status["spring_boot"] = True
    except Exception as e:
        logger.error("Spring Boot 상태 확인 실패", error=str(e))
    
    try:
        # Redis 상태 확인
        redis_client = await get_redis_client()
        health_status["redis"] = await redis_client.health_check()
    except Exception as e:
        logger.error("Redis 상태 확인 실패", error=str(e))
    
    return health_status

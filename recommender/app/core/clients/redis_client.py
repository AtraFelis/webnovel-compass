"""
Redis 클라이언트
추천 결과 캐싱 및 특징 벡터 저장을 담당합니다.
"""
import json
import redis.asyncio as redis
from typing import Optional, List, Dict, Any
from app.config import settings
from app.schemas import RecommendationResponse, NovelFeatures, NovelSimilarity
import structlog

logger = structlog.get_logger(__name__)


class RedisClient:
    """Redis 캐시 클라이언트"""
    
    def __init__(self):
        self.redis_url = settings.REDIS_URL
        self.cache_ttl = settings.CACHE_TTL
        self.redis_client: Optional[redis.Redis] = None
    
    async def connect(self):
        """Redis 연결"""
        try:
            self.redis_client = redis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True
            )
            # 연결 테스트
            await self.redis_client.ping()
            logger.info("Redis 연결 성공", url=self.redis_url)
        except Exception as e:
            logger.error("Redis 연결 실패", error=str(e))
            raise
    
    async def close(self):
        """Redis 연결 종료"""
        if self.redis_client:
            await self.redis_client.aclose()
            logger.info("Redis 연결 종료")
    
    async def _ensure_connected(self):
        """Redis 연결 확인"""
        if not self.redis_client:
            await self.connect()
    
    # === 추천 결과 캐싱 ===
    
    async def cache_user_recommendations(
        self, 
        user_id: int, 
        recommendations: RecommendationResponse
    ):
        """사용자 추천 결과 캐싱"""
        await self._ensure_connected()
        try:
            key = f"rec:user:{user_id}"
            value = recommendations.model_dump_json()
            await self.redis_client.setex(key, self.cache_ttl, value)
            logger.debug("추천 결과 캐시 저장", user_id=user_id, key=key)
        except Exception as e:
            logger.error("추천 결과 캐시 저장 실패", user_id=user_id, error=str(e))
    
    async def get_cached_user_recommendations(
        self, 
        user_id: int
    ) -> Optional[RecommendationResponse]:
        """사용자 추천 결과 캐시 조회"""
        await self._ensure_connected()
        try:
            key = f"rec:user:{user_id}"
            cached_data = await self.redis_client.get(key)
            if cached_data:
                data = json.loads(cached_data)
                return RecommendationResponse(**data)
            return None
        except Exception as e:
            logger.error("추천 결과 캐시 조회 실패", user_id=user_id, error=str(e))
            return None
    
    async def cache_similar_novels(
        self, 
        novel_id: int, 
        similar_novels: List[Dict[str, Any]]
    ):
        """유사 작품 목록 캐싱"""
        await self._ensure_connected()
        try:
            key = f"similar:novel:{novel_id}"
            value = json.dumps(similar_novels, ensure_ascii=False)
            await self.redis_client.setex(key, self.cache_ttl, value)
            logger.debug("유사 작품 캐시 저장", novel_id=novel_id, key=key)
        except Exception as e:
            logger.error("유사 작품 캐시 저장 실패", novel_id=novel_id, error=str(e))
    
    async def get_cached_similar_novels(
        self, 
        novel_id: int
    ) -> Optional[List[Dict[str, Any]]]:
        """유사 작품 목록 캐시 조회"""
        await self._ensure_connected()
        try:
            key = f"similar:novel:{novel_id}"
            cached_data = await self.redis_client.get(key)
            if cached_data:
                return json.loads(cached_data)
            return None
        except Exception as e:
            logger.error("유사 작품 캐시 조회 실패", novel_id=novel_id, error=str(e))
            return None
    
    # === 특징 벡터 저장 ===
    
    async def store_novel_features(self, novel_id: int, features: NovelFeatures):
        """웹소설 특징 벡터 저장"""
        await self._ensure_connected()
        try:
            key = f"features:novel:{novel_id}"
            value = features.model_dump_json()
            # 특징 벡터는 더 오래 캐시 (24시간)
            await self.redis_client.setex(key, 86400, value)
            logger.debug("특징 벡터 저장", novel_id=novel_id, key=key)
        except Exception as e:
            logger.error("특징 벡터 저장 실패", novel_id=novel_id, error=str(e))
    
    async def get_novel_features(self, novel_id: int) -> Optional[NovelFeatures]:
        """웹소설 특징 벡터 조회"""
        await self._ensure_connected()
        try:
            key = f"features:novel:{novel_id}"
            cached_data = await self.redis_client.get(key)
            if cached_data:
                data = json.loads(cached_data)
                return NovelFeatures(**data)
            return None
        except Exception as e:
            logger.error("특징 벡터 조회 실패", novel_id=novel_id, error=str(e))
            return None
    
    async def store_user_profile(self, user_id: int, profile: Dict[str, Any]):
        """사용자 취향 프로필 저장"""
        await self._ensure_connected()
        try:
            key = f"profile:user:{user_id}"
            value = json.dumps(profile, ensure_ascii=False)
            # 사용자 프로필은 더 오래 캐시 (12시간)
            await self.redis_client.setex(key, 43200, value)
            logger.debug("사용자 프로필 저장", user_id=user_id, key=key)
        except Exception as e:
            logger.error("사용자 프로필 저장 실패", user_id=user_id, error=str(e))
    
    async def get_user_profile(self, user_id: int) -> Optional[Dict[str, Any]]:
        """사용자 취향 프로필 조회"""
        await self._ensure_connected()
        try:
            key = f"profile:user:{user_id}"
            cached_data = await self.redis_client.get(key)
            if cached_data:
                return json.loads(cached_data)
            return None
        except Exception as e:
            logger.error("사용자 프로필 조회 실패", user_id=user_id, error=str(e))
            return None
    
    # === 유틸리티 메서드 ===
    
    async def clear_user_cache(self, user_id: int):
        """특정 사용자의 모든 캐시 삭제"""
        await self._ensure_connected()
        try:
            pattern = f"*:user:{user_id}"
            keys = await self.redis_client.keys(pattern)
            if keys:
                await self.redis_client.delete(*keys)
                logger.info("사용자 캐시 삭제", user_id=user_id, deleted_keys=len(keys))
        except Exception as e:
            logger.error("사용자 캐시 삭제 실패", user_id=user_id, error=str(e))
    
    async def health_check(self) -> bool:
        """Redis 연결 상태 확인"""
        try:
            await self._ensure_connected()
            await self.redis_client.ping()
            return True
        except Exception as e:
            logger.error("Redis 상태 확인 실패", error=str(e))
            return False

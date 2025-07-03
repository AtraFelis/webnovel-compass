"""
데이터 서비스
Spring Boot에서 데이터를 수집하고 전처리하는 비즈니스 로직
"""
from typing import List, Dict, Optional, Tuple
import asyncio
from app.core.clients import get_spring_client, get_redis_client
from app.schemas import User, Novel, UserRating, RecommendationType
import structlog

logger = structlog.get_logger(__name__)


class DataService:
    """데이터 수집 및 전처리 서비스"""
    
    def __init__(self):
        self.spring_client = None
        self.redis_client = None
    
    async def _init_clients(self):
        """클라이언트 초기화"""
        if not self.spring_client:
            self.spring_client = await get_spring_client()
        if not self.redis_client:
            self.redis_client = await get_redis_client()
    
    async def get_user_data(self, user_id: int) -> Optional[User]:
        """사용자 정보 조회"""
        await self._init_clients()
        try:
            user = await self.spring_client.get_user(user_id)
            if not user:
                logger.warning("사용자를 찾을 수 없음", user_id=user_id)
                return None
            
            logger.info("사용자 데이터 조회 성공", user_id=user_id, username=user.username)
            return user
            
        except Exception as e:
            logger.error("사용자 데이터 조회 실패", user_id=user_id, error=str(e))
            raise    
    async def get_user_rating_data(self, user_id: int) -> List[UserRating]:
        """사용자 평점 데이터 조회"""
        await self._init_clients()
        try:
            ratings = await self.spring_client.get_user_ratings(user_id)
            logger.info("사용자 평점 데이터 조회", user_id=user_id, rating_count=len(ratings))
            return ratings
            
        except Exception as e:
            logger.error("사용자 평점 데이터 조회 실패", user_id=user_id, error=str(e))
            return []
    
    async def get_novels_data(
        self, 
        limit: Optional[int] = None,
        genre: Optional[str] = None,
        min_rating: Optional[float] = None
    ) -> List[Novel]:
        """웹소설 목록 조회"""
        await self._init_clients()
        try:
            novels = await self.spring_client.get_novels(
                limit=limit, 
                genre=genre, 
                min_rating=min_rating
            )
            logger.info("웹소설 데이터 조회", novel_count=len(novels))
            return novels
            
        except Exception as e:
            logger.error("웹소설 데이터 조회 실패", error=str(e))
            return []
    
    async def get_all_rating_data(self) -> List[UserRating]:
        """전체 평점 데이터 조회 (협업 필터링용)"""
        await self._init_clients()
        try:
            ratings = await self.spring_client.get_all_ratings()
            logger.info("전체 평점 데이터 조회", total_ratings=len(ratings))
            return ratings
            
        except Exception as e:
            logger.error("전체 평점 데이터 조회 실패", error=str(e))
            return []
    
    async def collect_recommendation_data(
        self, 
        user_id: int
    ) -> Tuple[Optional[User], List[UserRating], List[Novel]]:
        """추천에 필요한 모든 데이터를 동시에 수집"""
        await self._init_clients()
        
        try:
            # 여러 API를 동시에 호출하여 성능 최적화
            user_task = self.spring_client.get_user(user_id)
            user_ratings_task = self.spring_client.get_user_ratings(user_id)
            novels_task = self.spring_client.get_novels()
            
            user, user_ratings, novels = await asyncio.gather(
                user_task,
                user_ratings_task, 
                novels_task,
                return_exceptions=True
            )
            
            # 에러 처리
            if isinstance(user, Exception):
                logger.error("사용자 데이터 수집 실패", user_id=user_id, error=str(user))
                user = None
                
            if isinstance(user_ratings, Exception):
                logger.error("사용자 평점 수집 실패", user_id=user_id, error=str(user_ratings))
                user_ratings = []
                
            if isinstance(novels, Exception):
                logger.error("웹소설 데이터 수집 실패", error=str(novels))
                novels = []
            
            logger.info(
                "추천 데이터 수집 완료",
                user_id=user_id,
                user_found=user is not None,
                user_ratings_count=len(user_ratings) if user_ratings else 0,
                novels_count=len(novels) if novels else 0
            )
            
            return user, user_ratings, novels
            
        except Exception as e:
            logger.error("추천 데이터 수집 중 오류", user_id=user_id, error=str(e))
            return None, [], []
    
    async def get_popular_novels(self, limit: int = 20) -> List[Novel]:
        """인기 웹소설 목록 조회"""
        await self._init_clients()
        try:
            novels = await self.spring_client.get_popular_novels(limit=limit)
            logger.info("인기 웹소설 조회 완료", count=len(novels))
            return novels
            
        except Exception as e:
            logger.error("인기 웹소설 조회 실패", error=str(e))
            return []
    
    async def get_novels_by_ids(self, novel_ids: List[int]) -> List[Novel]:
        """ID 목록으로 웹소설 정보 일괄 조회"""
        await self._init_clients()
        try:
            novels = await self.spring_client.batch_get_novels(novel_ids)
            logger.info("웹소설 일괄 조회 완료", requested=len(novel_ids), found=len(novels))
            return novels
            
        except Exception as e:
            logger.error("웹소설 일괄 조회 실패", novel_ids=len(novel_ids), error=str(e))
            return []

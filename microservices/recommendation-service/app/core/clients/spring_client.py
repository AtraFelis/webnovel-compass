"""
Spring Boot API 클라이언트
Spring Boot 백엔드와의 HTTP 통신을 담당합니다.
"""
import httpx
from typing import List, Optional, Dict, Any
from app.config import settings
from app.schemas import User, Novel, UserRating
import structlog

logger = structlog.get_logger(__name__)


class SpringBootClient:
    """Spring Boot API 클라이언트"""
    
    def __init__(self):
        self.base_url = settings.BACKEND_API_URL
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={"Content-Type": "application/json"}
        )
    
    async def close(self):
        """클라이언트 연결 종료"""
        await self.client.aclose()
    
    async def get_user(self, user_id: int) -> Optional[User]:
        """사용자 정보 조회"""
        try:
            response = await self.client.get(f"{self.base_url}/api/users/{user_id}")
            response.raise_for_status()
            
            user_data = response.json()
            return User(**user_data)
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                logger.warning("사용자를 찾을 수 없음", user_id=user_id)
                return None
            logger.error("사용자 조회 실패", user_id=user_id, error=str(e))
            raise
        except Exception as e:
            logger.error("사용자 조회 중 오류 발생", user_id=user_id, error=str(e))
            raise    
        
    async def get_user_ratings(self, user_id: int) -> List[UserRating]:
        """사용자의 평점 목록 조회"""
        try:
            response = await self.client.get(f"{self.base_url}/api/users/{user_id}/ratings")
            response.raise_for_status()
            
            ratings_data = response.json()
            return [UserRating(**rating) for rating in ratings_data]
            
        except httpx.HTTPStatusError as e:
            logger.error("사용자 평점 조회 실패", user_id=user_id, error=str(e))
            raise
        except Exception as e:
            logger.error("사용자 평점 조회 중 오류 발생", user_id=user_id, error=str(e))
            raise
    
    async def get_novel(self, novel_id: int) -> Optional[Novel]:
        """웹소설 정보 조회"""
        try:
            response = await self.client.get(f"{self.base_url}/api/novels/{novel_id}")
            response.raise_for_status()
            
            novel_data = response.json()
            return Novel(**novel_data)
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                logger.warning("웹소설을 찾을 수 없음", novel_id=novel_id)
                return None
            logger.error("웹소설 조회 실패", novel_id=novel_id, error=str(e))
            raise
        except Exception as e:
            logger.error("웹소설 조회 중 오류 발생", novel_id=novel_id, error=str(e))
            raise
    
    async def get_novels(
        self, 
        limit: Optional[int] = None,
        genre: Optional[str] = None,
        min_rating: Optional[float] = None
    ) -> List[Novel]:
        """웹소설 목록 조회"""
        try:
            params = {}
            if limit:
                params["limit"] = limit
            if genre:
                params["genre"] = genre
            if min_rating:
                params["minRating"] = min_rating
            
            response = await self.client.get(f"{self.base_url}/api/novels", params=params)
            response.raise_for_status()
            
            novels_data = response.json()
            return [Novel(**novel) for novel in novels_data]
            
        except Exception as e:
            logger.error("웹소설 목록 조회 중 오류 발생", error=str(e))
            raise
    
    async def get_all_ratings(self) -> List[UserRating]:
        """모든 사용자 평점 데이터 조회 (협업 필터링용)"""
        try:
            response = await self.client.get(f"{self.base_url}/api/ratings")
            response.raise_for_status()
            
            ratings_data = response.json()
            return [UserRating(**rating) for rating in ratings_data]
            
        except Exception as e:
            logger.error("전체 평점 데이터 조회 중 오류 발생", error=str(e))
            raise
    
    async def get_user_behaviors(self, user_id: int, days: int = 30) -> List[Dict[str, Any]]:
        """사용자 행동 데이터 조회 (조회, 클릭, 체류시간 등)"""
        try:
            params = {"days": days}
            response = await self.client.get(
                f"{self.base_url}/api/users/{user_id}/behaviors", 
                params=params
            )
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            logger.error("사용자 행동 데이터 조회 중 오류 발생", user_id=user_id, error=str(e))
            raise
    
    async def get_popular_novels(self, limit: int = 50) -> List[Novel]:
        """인기 웹소설 목록 조회"""
        try:
            params = {"limit": limit, "sortBy": "popularity"}
            response = await self.client.get(f"{self.base_url}/api/novels/popular", params=params)
            response.raise_for_status()
            
            novels_data = response.json()
            return [Novel(**novel) for novel in novels_data]
            
        except Exception as e:
            logger.error("인기 웹소설 조회 중 오류 발생", error=str(e))
            raise
    
    async def batch_get_novels(self, novel_ids: List[int]) -> List[Novel]:
        """여러 웹소설 정보 일괄 조회"""
        try:
            # POST 요청으로 ID 목록 전송
            response = await self.client.post(
                f"{self.base_url}/api/novels/batch",
                json={"novel_ids": novel_ids}
            )
            response.raise_for_status()
            
            novels_data = response.json()
            return [Novel(**novel) for novel in novels_data]
            
        except Exception as e:
            logger.error("웹소설 일괄 조회 중 오류 발생", novel_ids=len(novel_ids), error=str(e))
            raise

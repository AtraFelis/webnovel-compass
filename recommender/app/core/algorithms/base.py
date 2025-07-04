"""
추천 알고리즘 기본 인터페이스
"""
from abc import ABC, abstractmethod
from typing import List
from app.schemas import User, Novel, UserRating, RecommendationItem
import structlog

logger = structlog.get_logger(__name__)


class BaseRecommendationAlgorithm(ABC):
    """추천 알고리즘 기본 클래스"""
    
    @abstractmethod
    async def recommend(
        self, 
        user: User,
        user_ratings: List[UserRating], 
        novels: List[Novel],
        limit: int = 10
    ) -> List[RecommendationItem]:
        """
        추천 결과 생성
        
        Args:
            user: 사용자 정보
            user_ratings: 사용자 평점 목록
            novels: 전체 웹소설 목록
            limit: 추천 개수 제한
            
        Returns:
            추천 아이템 목록 (점수 순으로 정렬됨)
        """
        pass
    
    @abstractmethod
    def get_algorithm_name(self) -> str:
        """알고리즘 이름 반환"""
        pass
    
    def _create_recommendation_item(
        self, 
        novel: Novel, 
        score: float, 
        reason: str
    ) -> RecommendationItem:
        """추천 아이템 생성 헬퍼 메서드"""
        return RecommendationItem(
            novel_id=novel.id,
            title=novel.title,
            author=novel.author,
            genre=novel.genre,
            score=score,
            reason=reason,
            average_rating=novel.average_rating
        )
    
    def _log_algorithm_start(self, user_id: int):
        """알고리즘 시작 로깅"""
        logger.info(
            f"{self.get_algorithm_name()} 추천 시작", 
            user_id=user_id, 
            algorithm=self.get_algorithm_name()
        )
    
    def _log_algorithm_end(self, user_id: int, recommendation_count: int):
        """알고리즘 완료 로깅"""
        logger.info(
            f"{self.get_algorithm_name()} 추천 완료", 
            user_id=user_id, 
            algorithm=self.get_algorithm_name(),
            count=recommendation_count
        )

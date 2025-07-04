"""
인기 기반 추천 알고리즘
"""
from typing import List
from .base import BaseRecommendationAlgorithm
from app.schemas import User, Novel, UserRating, RecommendationItem


class PopularRecommendation(BaseRecommendationAlgorithm):
    """인기 기반 추천 알고리즘"""
    
    def get_algorithm_name(self) -> str:
        return "popular"
    
    async def recommend(
        self, 
        user: User,
        user_ratings: List[UserRating], 
        novels: List[Novel],
        limit: int = 10
    ) -> List[RecommendationItem]:
        """인기 기반 추천"""
        self._log_algorithm_start(user.id)
        
        recommendations = []
        rated_novel_ids = {rating.novel_id for rating in user_ratings}
        
        # 인기도 순으로 정렬 (평점 * 평점 개수)
        popular_novels = self._sort_by_popularity(novels)
        
        for novel in popular_novels:
            # 이미 평가한 작품 제외
            if novel.id in rated_novel_ids:
                continue
            
            # 인기도 점수 계산
            score = self._calculate_popularity_score(novel)
            
            recommendation = self._create_recommendation_item(
                novel, score, "인기 작품"
            )
            recommendations.append(recommendation)
            
            # 제한 개수에 도달하면 중단
            if len(recommendations) >= limit:
                break
        
        self._log_algorithm_end(user.id, len(recommendations))
        return recommendations
    
    def _sort_by_popularity(self, novels: List[Novel]) -> List[Novel]:
        """인기도 순으로 웹소설 정렬"""
        def popularity_key(novel):
            # 평점 * 평점 개수로 인기도 계산
            rating = novel.average_rating or 0
            count = novel.rating_count or 0
            return rating * count
        
        return sorted(novels, key=popularity_key, reverse=True)
    
    def _calculate_popularity_score(self, novel: Novel) -> float:
        """인기도 점수 계산 (0-1 범위)"""
        if not novel.average_rating:
            return 0.0
        
        # 평점을 5점 만점에서 1점 만점으로 정규화
        return novel.average_rating / 5.0

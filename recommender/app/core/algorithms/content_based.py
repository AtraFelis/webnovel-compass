"""
콘텐츠 기반 필터링 추천 알고리즘
"""
from typing import List
from .base import BaseRecommendationAlgorithm
from app.schemas import User, Novel, UserRating, RecommendationItem


class ContentBasedFiltering(BaseRecommendationAlgorithm):
    """콘텐츠 기반 필터링 추천 알고리즘"""
    
    def get_algorithm_name(self) -> str:
        return "content_based"
    
    async def recommend(
        self, 
        user: User,
        user_ratings: List[UserRating], 
        novels: List[Novel],
        limit: int = 10
    ) -> List[RecommendationItem]:
        """콘텐츠 기반 필터링 추천"""
        self._log_algorithm_start(user.id)
        
        recommendations = []
        rated_novel_ids = {rating.novel_id for rating in user_ratings}
        
        for novel in novels:
            # 이미 평가한 작품 제외
            if novel.id in rated_novel_ids:
                continue
            
            # 콘텐츠 기반 점수 계산
            score, reason_parts = self._calculate_content_score(user, novel)
            
            if score > 0:
                reason = " + ".join(reason_parts)
                recommendation = self._create_recommendation_item(
                    novel, score, reason
                )
                recommendations.append(recommendation)
        
        # 점수순 정렬 후 제한
        recommendations.sort(key=lambda x: x.score, reverse=True)
        result = recommendations[:limit]
        
        self._log_algorithm_end(user.id, len(result))
        return result
    
    def _calculate_content_score(
        self, 
        user: User, 
        novel: Novel
    ) -> tuple[float, List[str]]:
        """콘텐츠 기반 점수 계산"""
        score = 0.0
        reason_parts = []
        
        # 1. 장르 매칭 (가중치 0.6)
        if novel.genre in user.preferred_genres:
            score += 0.6
            reason_parts.append(f"선호 장르 '{novel.genre}'")
        
        # 2. 높은 평점 가중치 (가중치 0.3)
        if novel.average_rating and novel.average_rating >= 4.5:
            score += 0.3
            reason_parts.append("높은 평점 작품")
        
        # 3. 인기도 가중치 (가중치 0.1)
        if novel.rating_count >= 100:
            score += 0.1
            reason_parts.append("인기 작품")
        
        return score, reason_parts

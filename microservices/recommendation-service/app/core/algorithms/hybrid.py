"""
하이브리드 추천 알고리즘
"""
from typing import List, Dict
from .base import BaseRecommendationAlgorithm
from .collaborative_filtering import CollaborativeFiltering
from .content_based import ContentBasedFiltering
from app.schemas import User, Novel, UserRating, RecommendationItem


class HybridRecommendation(BaseRecommendationAlgorithm):
    """하이브리드 추천 알고리즘 (협업 필터링 + 콘텐츠 기반)"""
    
    def __init__(self, collab_weight: float = 0.6, content_weight: float = 0.4):
        """
        하이브리드 추천 초기화
        
        Args:
            collab_weight: 협업 필터링 가중치 (기본 0.6)
            content_weight: 콘텐츠 기반 가중치 (기본 0.4)
        """
        self.collab_weight = collab_weight
        self.content_weight = content_weight
        self.collaborative = CollaborativeFiltering()
        self.content_based = ContentBasedFiltering()
    
    def get_algorithm_name(self) -> str:
        return "hybrid"
    
    async def recommend(
        self, 
        user: User,
        user_ratings: List[UserRating], 
        novels: List[Novel],
        limit: int = 10
    ) -> List[RecommendationItem]:
        """하이브리드 추천 (협업 + 콘텐츠 기반 결합)"""
        self._log_algorithm_start(user.id)
        
        # 각 알고리즘별 추천 결과 수집 (더 많이 가져와서 결합)
        expanded_limit = limit * 2
        
        collab_recommendations = await self.collaborative.recommend(
            user, user_ratings, novels, expanded_limit
        )
        content_recommendations = await self.content_based.recommend(
            user, user_ratings, novels, expanded_limit
        )
        
        # 가중 평균으로 점수 결합
        combined_scores = self._combine_scores(
            collab_recommendations, content_recommendations
        )
        
        # 최종 추천 목록 생성
        final_recommendations = self._generate_final_recommendations(
            combined_scores, novels, limit
        )
        
        self._log_algorithm_end(user.id, len(final_recommendations))
        return final_recommendations
    
    def _combine_scores(
        self,
        collab_recommendations: List[RecommendationItem],
        content_recommendations: List[RecommendationItem]
    ) -> Dict[int, float]:
        """두 알고리즘의 점수를 가중 평균으로 결합"""
        novel_scores = {}
        
        # 협업 필터링 점수 (가중치 적용)
        for rec in collab_recommendations:
            novel_scores[rec.novel_id] = rec.score * self.collab_weight
        
        # 콘텐츠 기반 점수 (가중치 적용)
        for rec in content_recommendations:
            current_score = novel_scores.get(rec.novel_id, 0.0)
            novel_scores[rec.novel_id] = current_score + (rec.score * self.content_weight)
        
        return novel_scores
    
    def _generate_final_recommendations(
        self,
        combined_scores: Dict[int, float],
        novels: List[Novel],
        limit: int
    ) -> List[RecommendationItem]:
        """최종 추천 목록 생성"""
        recommendations = []
        novel_dict = {novel.id: novel for novel in novels}
        
        # 점수순으로 정렬
        sorted_novels = sorted(
            combined_scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        for novel_id, score in sorted_novels[:limit]:
            if novel_id in novel_dict:
                novel = novel_dict[novel_id]
                recommendation = self._create_recommendation_item(
                    novel, 
                    score,
                    f"하이브리드 추천 (협업:{self.collab_weight:.1f} + 콘텐츠:{self.content_weight:.1f})"
                )
                recommendations.append(recommendation)
        
        return recommendations

"""
협업 필터링 추천 알고리즘
"""
from typing import List, Dict
from .base import BaseRecommendationAlgorithm
from app.schemas import User, Novel, UserRating, RecommendationItem


class CollaborativeFiltering(BaseRecommendationAlgorithm):
    """협업 필터링 추천 알고리즘"""
    
    def get_algorithm_name(self) -> str:
        return "collaborative_filtering"
    
    async def recommend(
        self, 
        user: User,
        user_ratings: List[UserRating], 
        novels: List[Novel],
        limit: int = 10
    ) -> List[RecommendationItem]:
        """협업 필터링 기반 추천"""
        self._log_algorithm_start(user.id)
        
        if not user_ratings:
            # 평점이 없는 경우 빈 결과 반환
            self._log_algorithm_end(user.id, 0)
            return []
        
        # 사용자가 높게 평가한 장르 분석
        preferred_genres = self._analyze_preferred_genres(user_ratings, novels)
        
        # 선호 장르 기반 추천 생성
        recommendations = self._generate_genre_based_recommendations(
            preferred_genres, novels, user_ratings, limit
        )
        
        self._log_algorithm_end(user.id, len(recommendations))
        return recommendations
    
    def _analyze_preferred_genres(
        self, 
        user_ratings: List[UserRating], 
        novels: List[Novel]
    ) -> Dict[str, float]:
        """사용자 선호 장르 분석"""
        preferred_genres = {}
        novel_dict = {novel.id: novel for novel in novels}
        
        for rating in user_ratings:
            if rating.rating >= 4.0:  # 4점 이상만 고려
                novel = novel_dict.get(rating.novel_id)
                if novel:
                    genre_score = preferred_genres.get(novel.genre, 0.0)
                    preferred_genres[novel.genre] = genre_score + rating.rating
        
        # 정규화 (평점 개수로 나누기)
        if user_ratings:
            for genre in preferred_genres:
                preferred_genres[genre] /= len(user_ratings)
        
        return preferred_genres
    
    def _generate_genre_based_recommendations(
        self,
        preferred_genres: Dict[str, float],
        novels: List[Novel],
        user_ratings: List[UserRating],
        limit: int
    ) -> List[RecommendationItem]:
        """선호 장르 기반 추천 생성"""
        recommendations = []
        rated_novel_ids = {rating.novel_id for rating in user_ratings}
        
        for novel in novels:
            # 이미 평가한 작품 제외
            if novel.id in rated_novel_ids:
                continue
                
            # 선호 장르에 해당하는 작품만 추천
            if novel.genre in preferred_genres:
                score = preferred_genres[novel.genre]
                reason = f"선호 장르 '{novel.genre}' 기반 추천"
                
                recommendation = self._create_recommendation_item(
                    novel, min(score, 1.0), reason
                )
                recommendations.append(recommendation)
        
        # 점수순 정렬 후 제한
        recommendations.sort(key=lambda x: x.score, reverse=True)
        return recommendations[:limit]

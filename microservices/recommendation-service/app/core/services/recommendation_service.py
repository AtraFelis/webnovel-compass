"""
추천 서비스
추천 시스템의 핵심 비즈니스 로직을 담당합니다.
"""
from typing import List, Optional, Dict, Any
import asyncio
from datetime import datetime

from app.core.clients import get_redis_client
from app.schemas import (
    User, Novel, UserRating, 
    RecommendationRequest, RecommendationResponse, RecommendationItem,
    SimilarNovelRequest, RecommendationType
)
from .data_service import DataService
from app.core.algorithms import (
    CollaborativeFiltering,
    ContentBasedFiltering,
    HybridRecommendation,
    PopularRecommendation,
    SimilarityCalculator
)
import structlog

logger = structlog.get_logger(__name__)


class RecommendationService:
    """추천 시스템 핵심 서비스"""
    
    def __init__(self):
        self.data_service = DataService()
        self.redis_client = None
        
        # 추천 알고리즘 인스턴스 생성
        self.algorithms = {
            RecommendationType.COLLABORATIVE: CollaborativeFiltering(),
            RecommendationType.CONTENT_BASED: ContentBasedFiltering(),
            RecommendationType.HYBRID: HybridRecommendation(),
            RecommendationType.POPULAR: PopularRecommendation()
        }
    
    async def _init_clients(self):
        """클라이언트 초기화"""
        if not self.redis_client:
            self.redis_client = await get_redis_client()
    
    async def get_user_recommendations(
        self, 
        request: RecommendationRequest
    ) -> RecommendationResponse:
        """사용자 맞춤 추천 생성"""
        await self._init_clients()
        
        # 1. 캐시 확인
        cached_recommendations = await self.redis_client.get_cached_user_recommendations(
            request.user_id
        )
        if cached_recommendations:
            logger.info("캐시된 추천 결과 반환", user_id=request.user_id)
            return cached_recommendations
        
        # 2. 데이터 수집
        logger.info("사용자 추천 요청 처리 시작", user_id=request.user_id, type=request.recommendation_type)
        
        user, user_ratings, novels = await self.data_service.collect_recommendation_data(
            request.user_id
        )
        
        if not user:
            raise ValueError(f"사용자를 찾을 수 없습니다: {request.user_id}")
        
        # 3. 알고리즘 선택 및 실행
        algorithm = self.algorithms.get(request.recommendation_type)
        if not algorithm:
            # 기본값: 하이브리드 알고리즘
            algorithm = self.algorithms[RecommendationType.HYBRID]
        
        recommendations = await algorithm.recommend(
            user, user_ratings, novels, request.limit
        )
        
        # 4. 비즈니스 로직 필터링 적용
        filtered_recommendations = await self._apply_business_filters(
            recommendations, user_ratings, request
        )
        
        # 5. 응답 생성
        response = RecommendationResponse(
            user_id=request.user_id,
            recommendations=filtered_recommendations,
            total_count=len(filtered_recommendations),
            recommendation_type=request.recommendation_type,
            generated_at=datetime.now()
        )
        
        # 6. 캐시 저장
        await self.redis_client.cache_user_recommendations(request.user_id, response)
        
        logger.info(
            "사용자 추천 완료", 
            user_id=request.user_id, 
            recommendation_count=len(filtered_recommendations),
            type=request.recommendation_type
        )
        
        return response
    
    async def _apply_business_filters(
        self,
        recommendations: List[RecommendationItem],
        user_ratings: List[UserRating],
        request: RecommendationRequest
    ) -> List[RecommendationItem]:
        """비즈니스 로직 필터링 적용"""
        filtered_recommendations = recommendations
        
        # 읽은 작품 필터링
        if request.exclude_read and user_ratings:
            read_novel_ids = {rating.novel_id for rating in user_ratings}
            filtered_recommendations = [
                rec for rec in filtered_recommendations 
                if rec.novel_id not in read_novel_ids
            ]
        
        # 최소 평점 필터링
        if request.min_rating:
            filtered_recommendations = [
                rec for rec in filtered_recommendations
                if rec.average_rating and rec.average_rating >= request.min_rating
            ]
        
        # 결과 제한
        return filtered_recommendations[:request.limit]
    
    async def get_similar_novels(
        self, 
        request: SimilarNovelRequest
    ) -> List[RecommendationItem]:
        """유사 작품 추천"""
        await self._init_clients()
        
        # 캐시 확인
        cached_similar = await self.redis_client.get_cached_similar_novels(request.novel_id)
        if cached_similar:
            logger.info("캐시된 유사 작품 반환", novel_id=request.novel_id)
            return [RecommendationItem(**item) for item in cached_similar[:request.limit]]
        
        logger.info("유사 작품 추천 시작", novel_id=request.novel_id)
        
        # 기준 웹소설 정보 조회
        base_novel = await self.data_service.spring_client.get_novel(request.novel_id)
        if not base_novel:
            raise ValueError(f"웹소설을 찾을 수 없습니다: {request.novel_id}")
        
        # 같은 장르의 웹소설들 조회
        candidate_novels = await self.data_service.get_novels_data(
            genre=base_novel.genre,
            limit=100
        )
        
        # 유사도 계산 및 추천 생성
        similar_novels_with_scores = SimilarityCalculator.find_similar_novels(
            base_novel,
            candidate_novels,
            request.similarity_threshold,
            request.limit
        )
        
        # RecommendationItem으로 변환
        recommendations = []
        for similar_novel, similarity_score in similar_novels_with_scores:
            recommendation = RecommendationItem(
                novel_id=similar_novel.id,
                title=similar_novel.title,
                author=similar_novel.author,
                genre=similar_novel.genre,
                score=similarity_score,
                reason=f"'{base_novel.title}'와 유사한 작품",
                average_rating=similar_novel.average_rating
            )
            recommendations.append(recommendation)
        
        # 캐시 저장
        cache_data = [rec.model_dump() for rec in recommendations]
        await self.redis_client.cache_similar_novels(request.novel_id, cache_data)
        
        logger.info("유사 작품 추천 완료", novel_id=request.novel_id, count=len(recommendations))
        
        return recommendations

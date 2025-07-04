"""
추천 시스템 API 엔드포인트
"""
from fastapi import APIRouter, HTTPException, Depends, Path
from typing import List

from app.schemas import (
    RecommendationRequest, 
    RecommendationResponse,
    SimilarNovelRequest,
    RecommendationItem
)
from app.core.services import RecommendationService
import structlog

logger = structlog.get_logger(__name__)

router = APIRouter()

# 의존성 주입용 서비스 인스턴스
def get_recommendation_service() -> RecommendationService:
    return RecommendationService()


@router.post(
    "/users/{user_id}/recommendations",
    response_model=RecommendationResponse,
    summary="사용자 맞춤 추천",
    description="사용자 ID를 기반으로 개인화된 웹소설 추천 목록을 제공합니다."
)
async def get_user_recommendations(
    request: RecommendationRequest,
    user_id: int = Path(..., description="추천받을 사용자 ID"),
    service: RecommendationService = Depends(get_recommendation_service)
) -> RecommendationResponse:
    """
    사용자 맞춤 추천 API
    
    - **user_id**: 추천받을 사용자 ID (URL 경로에서)
    - **limit**: 추천 개수 (기본 10개, 최대 50개)
    - **recommendation_type**: 추천 타입 (collaborative, content_based, hybrid, popular)
    - **exclude_read**: 읽은 작품 제외 여부 (기본 True)
    - **min_rating**: 최소 평점 필터 (1-5점)
    """
    try:
        # URL의 user_id를 request에 설정
        request.user_id = user_id
        
        logger.info(
            "추천 API 요청", 
            user_id=user_id, 
            type=request.recommendation_type,
            limit=request.limit
        )
        
        response = await service.get_user_recommendations(request)
        
        logger.info(
            "추천 API 응답 성공",
            user_id=user_id,
            recommendation_count=len(response.recommendations)
        )
        
        return response
        
    except ValueError as e:
        logger.warning("추천 요청 검증 실패", user_id=user_id, error=str(e))
        raise HTTPException(status_code=404, detail=str(e))
        
    except Exception as e:
        logger.error("추천 API 처리 중 오류", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=500, 
            detail="추천 처리 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
        )


@router.get(
    "/users/{user_id}/recommendations",
    response_model=RecommendationResponse,
    summary="사용자 추천 (GET 방식)",
    description="GET 방식으로 사용자 맞춤 추천을 제공합니다. 간단한 파라미터만 지원합니다."
)
async def get_user_recommendations_simple(
    user_id: int = Path(..., description="추천받을 사용자 ID"),
    limit: int = 10,
    exclude_read: bool = True,
    service: RecommendationService = Depends(get_recommendation_service)
) -> RecommendationResponse:
    """
    간단한 사용자 추천 API (GET 방식)
    
    - **user_id**: 추천받을 사용자 ID (URL 경로에서)
    - **limit**: 추천 개수 (기본 10개)
    - **exclude_read**: 읽은 작품 제외 여부 (기본 True)
    """
    try:
        # RecommendationRequest 객체 생성
        request = RecommendationRequest(
            user_id=user_id,
            limit=min(limit, 50),  # 최대 50개로 제한
            exclude_read=exclude_read
        )
        
        logger.info("간단 추천 API 요청", user_id=user_id, limit=limit)
        
        response = await service.get_user_recommendations(request)
        
        return response
        
    except ValueError as e:
        logger.warning("간단 추천 요청 검증 실패", user_id=user_id, error=str(e))
        raise HTTPException(status_code=404, detail=str(e))
        
    except Exception as e:
        logger.error("간단 추천 API 처리 중 오류", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=500,
            detail="추천 처리 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
        )


@router.post(
    "/novels/{novel_id}/similar",
    response_model=List[RecommendationItem],
    summary="유사 작품 추천",
    description="특정 웹소설과 유사한 작품들을 추천합니다."
)
async def get_similar_novels(
    request: SimilarNovelRequest,
    novel_id: int = Path(..., description="기준이 되는 웹소설 ID"),
    service: RecommendationService = Depends(get_recommendation_service)
) -> List[RecommendationItem]:
    """
    유사 작품 추천 API
    
    - **novel_id**: 기준이 되는 웹소설 ID (URL 경로에서)
    - **limit**: 추천 개수 (기본 10개, 최대 50개)  
    - **similarity_threshold**: 유사도 임계값 (0.0-1.0, 기본 0.1)
    """
    try:
        # URL의 novel_id를 request에 설정
        request.novel_id = novel_id
        
        logger.info(
            "유사 작품 추천 API 요청",
            novel_id=novel_id,
            limit=request.limit,
            threshold=request.similarity_threshold
        )
        
        recommendations = await service.get_similar_novels(request)
        
        logger.info(
            "유사 작품 추천 API 응답 성공",
            novel_id=novel_id,
            recommendation_count=len(recommendations)
        )
        
        return recommendations
        
    except ValueError as e:
        logger.warning("유사 작품 요청 검증 실패", novel_id=novel_id, error=str(e))
        raise HTTPException(status_code=404, detail=str(e))
        
    except Exception as e:
        logger.error("유사 작품 API 처리 중 오류", novel_id=novel_id, error=str(e))
        raise HTTPException(
            status_code=500,
            detail="유사 작품 추천 처리 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
        )


@router.get(
    "/novels/{novel_id}/similar",
    response_model=List[RecommendationItem],
    summary="유사 작품 추천 (GET 방식)",
    description="GET 방식으로 유사한 작품들을 추천합니다."
)
async def get_similar_novels_simple(
    novel_id: int = Path(..., description="기준이 되는 웹소설 ID"),
    limit: int = 10,
    similarity_threshold: float = 0.1,
    service: RecommendationService = Depends(get_recommendation_service)
) -> List[RecommendationItem]:
    """
    간단한 유사 작품 추천 API (GET 방식)
    
    - **novel_id**: 기준이 되는 웹소설 ID (URL 경로에서)
    - **limit**: 추천 개수 (기본 10개)
    - **similarity_threshold**: 유사도 임계값 (기본 0.1)
    """
    try:
        # SimilarNovelRequest 객체 생성
        request = SimilarNovelRequest(
            novel_id=novel_id,
            limit=min(limit, 50),  # 최대 50개로 제한
            similarity_threshold=similarity_threshold
        )
        
        logger.info("간단 유사 작품 API 요청", novel_id=novel_id, limit=limit)
        
        recommendations = await service.get_similar_novels(request)
        
        return recommendations
        
    except ValueError as e:
        logger.warning("간단 유사 작품 요청 검증 실패", novel_id=novel_id, error=str(e))
        raise HTTPException(status_code=404, detail=str(e))
        
    except Exception as e:
        logger.error("간단 유사 작품 API 처리 중 오류", novel_id=novel_id, error=str(e))
        raise HTTPException(
            status_code=500,
            detail="유사 작품 추천 처리 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
        )

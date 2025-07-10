"""
테스트 및 개발용 API 엔드포인트
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from app.schemas import Novel, User, UserRating
import structlog

logger = structlog.get_logger(__name__)

router = APIRouter()


@router.get(
    "/dummy-data",
    summary="더미 데이터 생성",
    description="테스트용 더미 데이터를 생성합니다."
)
async def create_dummy_data() -> Dict[str, Any]:
    """
    테스트용 더미 데이터 생성
    """
    # 더미 사용자
    dummy_users = [
        User(
            id=1,
            username="독서광123",
            email="reader123@example.com",
            age=25,
            preferred_genres=["로맨스", "판타지"],
            created_at="2024-01-01T00:00:00"
        ),
        User(
            id=2, 
            username="소설매니아",
            email="novel@example.com",
            age=30,
            preferred_genres=["액션", "무협"],
            created_at="2024-01-02T00:00:00"
        )
    ]
    
    # 더미 웹소설
    dummy_novels = [
        Novel(
            id=1,
            title="판타지 대모험",
            author="작가A",
            description="마법과 모험이 가득한 판타지 소설",
            genre="판타지",
            tags=["마법", "모험", "용사"],
            average_rating=4.5,
            rating_count=150,
            view_count=1000,
            created_at="2024-01-01T00:00:00",
            updated_at="2024-01-01T00:00:00"
        ),
        Novel(
            id=2,
            title="달콤한 로맨스",
            author="작가B", 
            description="설렘 가득한 로맨스 스토리",
            genre="로맨스",
            tags=["달콤", "설렘", "사랑"],
            average_rating=4.2,
            rating_count=200,
            view_count=1500,
            created_at="2024-01-02T00:00:00",
            updated_at="2024-01-02T00:00:00"
        )
    ]
    
    # 더미 평점
    dummy_ratings = [
        UserRating(
            user_id=1,
            novel_id=1,
            rating=4.5,
            created_at="2024-01-01T00:00:00"
        ),
        UserRating(
            user_id=1,
            novel_id=2, 
            rating=4.0,
            created_at="2024-01-02T00:00:00"
        )
    ]
    
    return {
        "message": "더미 데이터 생성 완료",
        "data": {
            "users": [user.model_dump() for user in dummy_users],
            "novels": [novel.model_dump() for novel in dummy_novels],
            "ratings": [rating.model_dump() for rating in dummy_ratings]
        }
    }


@router.get(
    "/api-info",
    summary="API 정보",
    description="현재 구현된 API 엔드포인트 정보를 제공합니다."
)
async def get_api_info() -> Dict[str, Any]:
    """
    API 정보 조회
    """
    return {
        "service": "웹소설나침반 추천 서비스",
        "version": "0.1.0",
        "endpoints": {
            "recommendations": {
                "POST /api/recommender/v1/users/{user_id}/recommendations\": \"사용자 맞춤 추천 (상세)",
                "GET /api/recommender/v1/users/{user_id}/recommendations\": \"사용자 맞춤 추천 (간단)",
                "POST /api/recommender/v1/novels/{novel_id}/similar\": \"유사 작품 추천 (상세)",
                "GET /api/recommender/v1/novels/{novel_id}/similar\": \"유사 작품 추천 (간단)"
            },
            "health": {
                "GET /api/recommender/v1/health\": \"상세 헬스체크",
                "GET /api/recommender/v1/health/simple\": \"간단한 헬스체크"
            },
            "test": {
                "GET /api/recommender/v1/test/dummy-data\": \"더미 데이터 생성",
                "GET /api/recommender/v1/test/api-info\": \"API 정보"
            }
        },
        "features": [
            "협업 필터링 추천",
            "콘텐츠 기반 추천", 
            "하이브리드 추천",
            "인기 기반 추천",
            "유사 작품 추천",
            "Redis 캐싱",
            "Spring Boot 연동"
        ]
    }

"""
Pydantic 스키마 모듈
"""

# 웹소설 관련 모델
from .novel import (
    Novel,
    NovelBase,
    NovelCreate,
    NovelUpdate,
    NovelFeatures,
    NovelSimilarity
)

# 사용자 관련 모델
from .user import (
    User,
    UserBase,
    UserCreate,
    UserUpdate,
    UserRating
)

# 추천 시스템 관련 모델
from .recommendation import (
    RecommendationType,
    RecommendationRequest,
    SimilarNovelRequest,
    RecommendationItem,
    RecommendationResponse
)

__all__ = [
    # 웹소설 모델
    "Novel",
    "NovelBase", 
    "NovelCreate",
    "NovelUpdate",
    "NovelFeatures",
    "NovelSimilarity",
    
    # 사용자 모델
    "User",
    "UserBase",
    "UserCreate", 
    "UserUpdate",
    "UserRating",
    
    # 추천 모델
    "RecommendationType",
    "RecommendationRequest",
    "SimilarNovelRequest", 
    "RecommendationItem",
    "RecommendationResponse"
]

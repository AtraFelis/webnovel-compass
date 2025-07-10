"""
추천 시스템 관련 Pydantic 모델
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class RecommendationType(str, Enum):
    """추천 타입"""
    COLLABORATIVE = "collaborative"  # 협업 필터링
    CONTENT_BASED = "content_based"  # 콘텐츠 기반
    HYBRID = "hybrid"  # 하이브리드
    POPULAR = "popular"  # 인기순
    SIMILAR = "similar"  # 유사 작품


class RecommendationRequest(BaseModel):
    """추천 요청"""
    user_id: int = Field(..., description="사용자 ID")
    limit: int = Field(10, ge=1, le=50, description="추천 개수")
    recommendation_type: Optional[RecommendationType] = Field(
        RecommendationType.HYBRID, 
        description="추천 타입"
    )
    exclude_read: bool = Field(True, description="읽은 작품 제외")
    min_rating: Optional[float] = Field(None, ge=1.0, le=5.0, description="최소 평점")


class SimilarNovelRequest(BaseModel):
    """유사 작품 추천 요청"""
    novel_id: int = Field(..., description="기준 웹소설 ID")
    limit: int = Field(10, ge=1, le=50, description="추천 개수")
    similarity_threshold: float = Field(0.1, ge=0.0, le=1.0, description="유사도 임계값")


class RecommendationItem(BaseModel):
    """추천 아이템"""
    novel_id: int = Field(..., description="웹소설 ID")
    title: str = Field(..., description="웹소설 제목")
    author: str = Field(..., description="작가명")
    genre: str = Field(..., description="장르")
    score: float = Field(..., description="추천 점수")
    reason: Optional[str] = Field(None, description="추천 이유")
    average_rating: Optional[float] = Field(None, description="평균 평점")
    
    class Config:
        from_attributes = True


class RecommendationResponse(BaseModel):
    """추천 응답"""
    user_id: int = Field(..., description="사용자 ID")
    recommendations: List[RecommendationItem] = Field(..., description="추천 목록")
    total_count: int = Field(..., description="총 추천 개수")
    recommendation_type: RecommendationType = Field(..., description="사용된 추천 타입")
    generated_at: datetime = Field(default_factory=datetime.now, description="생성 시간")
    
    class Config:
        from_attributes = True
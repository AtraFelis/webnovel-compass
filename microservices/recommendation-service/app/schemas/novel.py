"""
웹소설 관련 Pydantic 모델
"""
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class NovelBase(BaseModel):
    """웹소설 기본 정보"""
    title: str = Field(..., description="웹소설 제목")
    author: str = Field(..., description="작가명")
    description: Optional[str] = Field(None, description="줄거리")
    genre: str = Field(..., description="장르")
    tags: List[str] = Field(default_factory=list, description="태그 목록")
    status: str = Field("연재중", description="연재 상태")
    total_chapters: Optional[int] = Field(None, description="총 화수")


class Novel(NovelBase):
    """웹소설 전체 정보"""
    id: int = Field(..., description="웹소설 ID")
    average_rating: Optional[float] = Field(None, description="평균 평점")
    rating_count: int = Field(0, description="평점 개수")
    view_count: int = Field(0, description="조회수")
    created_at: datetime = Field(..., description="등록일")
    updated_at: datetime = Field(..., description="수정일")

    class Config:
        from_attributes = True


class NovelCreate(NovelBase):
    """웹소설 생성 요청"""
    pass


class NovelUpdate(BaseModel):
    """웹소설 수정 요청"""
    title: Optional[str] = None
    description: Optional[str] = None
    genre: Optional[str] = None
    tags: Optional[List[str]] = None
    status: Optional[str] = None
    total_chapters: Optional[int] = None


class NovelFeatures(BaseModel):
    """웹소설 특징 벡터 (콘텐츠 기반 필터링용)"""
    novel_id: int = Field(..., description="웹소설 ID")
    genre_vector: List[float] = Field(..., description="장르 특징 벡터")
    tag_vector: List[float] = Field(..., description="태그 특징 벡터")
    text_features: List[float] = Field(..., description="텍스트 특징 벡터 (TF-IDF)")
    
    class Config:
        from_attributes = True


class NovelSimilarity(BaseModel):
    """웹소설 유사도 정보"""
    novel_id: int = Field(..., description="웹소설 ID")
    similar_novels: List[int] = Field(..., description="유사한 웹소설 ID 목록")
    similarity_scores: List[float] = Field(..., description="유사도 점수 목록")
    
    class Config:
        from_attributes = True

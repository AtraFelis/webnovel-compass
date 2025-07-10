"""
사용자 관련 Pydantic 모델
"""
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from datetime import datetime


class UserBase(BaseModel):
    """사용자 기본 정보"""
    username: str = Field(..., description="사용자명")
    email: str = Field(..., description="이메일")
    age: Optional[int] = Field(None, description="나이")
    preferred_genres: List[str] = Field(default_factory=list, description="선호 장르")


class User(UserBase):
    """사용자 전체 정보"""
    id: int = Field(..., description="사용자 ID")
    created_at: datetime = Field(..., description="가입일")
    last_active: Optional[datetime] = Field(None, description="마지막 활동일")
    
    class Config:
        from_attributes = True


class UserCreate(UserBase):
    """사용자 생성 요청"""
    pass


class UserUpdate(BaseModel):
    """사용자 수정 요청"""
    username: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    preferred_genres: Optional[List[str]] = None


class UserRating(BaseModel):
    """사용자 평점 정보"""
    user_id: int = Field(..., description="사용자 ID")
    novel_id: int = Field(..., description="웹소설 ID")
    rating: float = Field(..., ge=1.0, le=5.0, description="평점 (1-5)")
    created_at: datetime = Field(..., description="평점 등록일")
    
    class Config:
        from_attributes = True
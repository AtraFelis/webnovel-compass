from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """애플리케이션 설정"""
    
    # 기본 설정
    PROJECT_NAME: str = "웹소설나침반 추천 서비스"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/recommender/v1"
    
    # 서버 설정
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # 데이터베이스 설정
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/webnovel_compass"
    
    # Redis 설정
    REDIS_URL: str = "redis://localhost:6379"
    
    # Spring Boot 백엔드 연동
    BACKEND_API_URL: str = "http://localhost:8080"
    
    # ML 모델 설정
    MODEL_UPDATE_INTERVAL: int = 3600  # 1시간 (초 단위)
    RECOMMENDATION_COUNT: int = 10
    MIN_RATING_COUNT: int = 5  # 추천에 필요한 최소 평점 수
    
    # 캐싱 설정
    CACHE_TTL: int = 1800  # 30분 (초 단위)
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


# 전역 설정 인스턴스
settings = Settings()

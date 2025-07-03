from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.config import settings
from app.api.v1.api import api_router
from app.core.clients import close_clients
import structlog

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 라이프사이클 관리"""
    # 시작 시
    logger.info("웹소설나침반 추천 서비스 시작", version=settings.VERSION)
    yield
    # 종료 시
    logger.info("웹소설나침반 추천 서비스 종료")
    await close_clients()


# FastAPI 앱 생성
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI 기반 웹소설 추천 시스템",
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# API 라우터 등록
app.include_router(api_router, prefix=settings.API_V1_STR)

# 루트 엔드포인트
@app.get("/")
async def root():
    return {
        "message": "웹소설나침반 추천 서비스",
        "status": "running",
        "version": settings.VERSION,
        "api_docs": f"{settings.API_V1_STR}/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
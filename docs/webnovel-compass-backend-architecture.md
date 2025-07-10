# 웹소설나침반 - 백엔드 아키텍처 문서

## 📋 프로젝트 개요

**프로젝트명**: 웹소설나침반 (WebNovel Compass)  
**목적**: AI 기반 개인화 웹소설 추천 시스템  
**아키텍처**: 단일 서버 마이크로서비스  
**개발 목적**: 학습 및 실무 경험  

---

## 🏗️ 시스템 아키텍처

### 전체 구조도
```
[프론트엔드] → [API Gateway:8080] → [Eureka Server:8761]
                        ↓
    ┌─────────────────────────────────────────────┐
    │                마이크로서비스들                │
    │  ┌─────────────┬─────────────┬─────────────┐  │
    │  │ User Service│Content Svc  │Analytics Svc│  │
    │  │   :8081     │   :8082     │   :8083     │  │
    │  └─────────────┴─────────────┴─────────────┘  │
    │  ┌─────────────────────────────────────────┐  │
    │  │    Recommendation Service (Python)     │  │
    │  │              :8084                     │  │
    │  └─────────────────────────────────────────┘  │
    └─────────────────────────────────────────────┘
                        ↓
    ┌─────────────────────────────────────────────┐
    │              데이터 레이어                    │
    │  PostgreSQL     Redis        Elasticsearch  │
    │    :5432       :6379           :9200        │
    └─────────────────────────────────────────────┘
```

---

## 🎯 마이크로서비스 구성

### 1️⃣ Eureka Server (Service Discovery)
```yaml
포트: 8761
기술스택: Spring Boot 3.2 + Netflix Eureka
역할:
  - 마이크로서비스 등록 및 발견
  - 서비스 상태 모니터링
  - 로드 밸런싱 지원
  - 서비스 헬스체크

설정:
  - 자기 자신은 Eureka에 등록하지 않음
  - 개발환경에서 self-preservation 비활성화
  - 대시보드 제공 (http://localhost:8761)
```

### 2️⃣ User Service (사용자 관리)
```yaml
포트: 8081
기술스택: Spring Boot 3.2 + JPA + PostgreSQL + Spring Security
데이터베이스: userdb (PostgreSQL)

주요 기능:
  - 사용자 인증/인가 (JWT)
  - 회원가입, 로그인, 프로필 관리
  - 사용자 취향 설정 관리
  - 소셜 로그인 연동 (Google, Naver, Kakao)

핵심 엔티티:
  - User, UserProfile, UserPreferences
  - UserSession, SocialAccount
```

### 3️⃣ Content Service (콘텐츠 관리)
```yaml
포트: 8082
기술스택: Spring Boot 3.2 + JPA + Elasticsearch
데이터베이스: contentdb (PostgreSQL) + Elasticsearch

주요 기능:
  - 웹소설 메타데이터 관리 (제목, 작가, 장르, 줄거리)
  - 평점/리뷰 시스템 (1-5점 평점, 텍스트 리뷰)
  - 검색 및 필터링 (Elasticsearch 기반)
  - 콘텐츠 통계 관리
  - 스포일러 관리 및 모더레이션

핵심 엔티티:
  - Novel, Author, Genre, Tag
  - UserRating, UserReview, NovelStatistics
```

### 4️⃣ Analytics Service (행동 분석)
```yaml
포트: 8083
기술스택: Spring Boot 3.2 + WebFlux + Redis
데이터베이스: analyticsdb (PostgreSQL) + Redis

주요 기능:
  - 사용자 행동 이벤트 수집 (10ms 이하 응답)
  - 실시간 스트림 처리 (초당 10,000개 이벤트)
  - 세션 관리 및 추적 (30분 타임아웃)
  - 통계 분석 및 리포팅
  - 추천 효과 측정

핵심 컴포넌트:
  - Event Collector API (비동기 처리)
  - Session Manager (Redis 기반)
  - Real-time Analytics Engine
  - Batch Analytics Engine
```

### 5️⃣ Recommendation Service (AI 추천)
```yaml
포트: 8084
기술스택: Python 3.11 + FastAPI + scikit-learn
데이터베이스: PostgreSQL (모델 메타데이터) + Redis (캐싱)

주요 기능:
  - AI 추천 알고리즘 (협업 필터링 + 콘텐츠 기반)
  - 개인화 추천 생성 (200ms 이하)
  - 모델 학습 및 업데이트
  - 추천 성능 측정 (Precision@10 > 15%)

추천 알고리즘:
  - 협업 필터링: 사용자 기반, 아이템 기반, 매트릭스 팩토라이제이션
  - 콘텐츠 기반: 장르, 태그, TF-IDF 기반 줄거리 분석
  - 하이브리드: 가중 평균 (협업 60% + 콘텐츠 40%)
```

---

## 💾 데이터 저장소 전략

### Database per Service 원칙
```yaml
User Service:
  - userdb (PostgreSQL): 사용자 정보, 세션, 취향 데이터

Content Service:
  - contentdb (PostgreSQL): 웹소설 메타데이터, 평점, 리뷰
  - Elasticsearch: 검색 인덱스, 전문 검색

Analytics Service:
  - analyticsdb (PostgreSQL): 배치 분석 결과
  - Redis: 실시간 세션, 이벤트 스트리밍

Recommendation Service:
  - PostgreSQL: 모델 메타데이터, 추천 이력
  - Redis: 추천 결과 캐시, 유사도 매트릭스
```

### PostgreSQL 다중 데이터베이스 설정
```sql
-- Docker 컨테이너 환경변수
POSTGRES_MULTIPLE_DATABASES: userdb,contentdb,analyticsdb

-- 자동 생성 스크립트: database/init/create-multiple-databases.sh
```

---

## 🔄 서비스 간 통신

### 1️⃣ Service Discovery
```yaml
방식: Netflix Eureka
- 모든 서비스가 Eureka Server에 자동 등록
- 클라이언트 사이드 로드 밸런싱
- 서비스명으로 동적 통신 (user-service, content-service)
```

### 2️⃣ 동기 통신 (REST API)
```yaml
방식: OpenFeign + RestTemplate
예시:
  - Content Service → User Service (사용자 정보 조회)
  - API Gateway → 각 서비스 (라우팅)

설정:
  - Circuit Breaker: Hystrix/Resilience4j
  - Timeout: 2초
  - Retry: 3회
```

### 3️⃣ 비동기 통신 (Event-Driven)
```yaml
방식: Redis Pub/Sub (Kafka 대신 단순화)
이벤트 플로우:
  1. 사용자 행동 → Analytics Service → Redis Pub/Sub
  2. Redis Streams → Recommendation Service
  3. 모델 업데이트 → 추천 결과 갱신

장점:
  - Kafka보다 단순한 설정
  - 단일 서버 환경에 적합
  - 리소스 효율적
```

---

## 🐳 컨테이너 구성

### Docker Compose 설정
```yaml
services:
  # Infrastructure
  eureka-server:    # :8761
  api-gateway:      # :8080 (향후 추가)
  
  # Microservices  
  user-service:     # :8081
  content-service:  # :8082
  analytics-service: # :8083
  recommendation-service: # :8084
  
  # Databases
  postgres:         # :5432 (다중 DB)
  redis:           # :6379 
  elasticsearch:   # :9200 (Single Node)

리소스 제한:
  - 각 서비스: 512MB 메모리 제한
  - PostgreSQL: 512MB
  - Redis: 256MB
  - 총 사용량: ~3.3GB
```

---

## 🔒 보안 및 설정

### 인증/인가 전략
```yaml
JWT 토큰 기반:
  - Access Token: 15분 (짧은 유효기간)
  - Refresh Token: 7일
  - 토큰 검증: API Gateway에서 중앙화

소셜 로그인:
  - OAuth 2.0: Google, Naver, Kakao
  - 연동 정보: User Service에서 관리
```

### 환경변수 관리
```yaml
공통 설정:
  - Eureka Server URL: http://eureka-server:8761/eureka/
  - PostgreSQL 접속 정보
  - Redis 접속 정보

서비스별 설정:
  - 포트 번호 (8081-8084)
  - 데이터베이스 이름
  - JWT Secret Key
```

---

## 📊 성능 목표

### 응답 시간 목표
```yaml
User Service:      < 200ms (인증 API)
Content Service:   < 200ms (검색 API)
Analytics Service: < 10ms  (이벤트 수집)
Recommendation:    < 200ms (추천 생성)
```

### 처리량 목표
```yaml
동시 사용자:       1,000명 이상
이벤트 처리:       초당 10,000개
추천 정확도:       Precision@10 > 15%
시스템 가용성:     99.9% 이상
```

---

## 🚀 개발 진행 상황

### ✅ 완료된 단계
1. **Eureka Server** - 서비스 디스커버리 구축 완료
2. **User Service** - 사용자 관리 서비스 구현 완료
3. **프로젝트 구조** - 마이크로서비스 폴더 구조 완성

### 🔄 진행 중
3. **Content Service** - 웹소설 메타데이터 관리 서비스 구현 중
4. **PostgreSQL 다중 DB** - 자동 생성 스크립트 작성 중

### 📝 예정된 단계
4. **Analytics Service** - 사용자 행동 분석 서비스
5. **Recommendation Service** - Python 기반 AI 추천 엔진
6. **API Gateway** - 통합 진입점 및 라우팅
7. **서비스 간 통신** - REST API + Redis Pub/Sub 연동
8. **프론트엔드 연동** - React와 백엔드 API 통합

---

## 🎯 설계 원칙

### 마이크로서비스 원칙
- **단일 책임**: 각 서비스는 하나의 비즈니스 도메인 담당
- **독립 배포**: 서비스별 독립적인 개발 및 배포
- **데이터 독립성**: Database per Service 패턴
- **장애 격리**: Circuit Breaker로 장애 전파 방지

### 학습 목적 고려사항
- **단순화**: Kafka → Redis Pub/Sub로 복잡도 감소
- **단일 서버**: 클러스터 대신 단일 인스턴스로 리소스 절약
- **실무 패턴**: 실제 프로덕션에서 사용되는 패턴 적용
- **확장 가능**: 향후 프로덕션 환경으로 확장 가능한 구조

---

*문서 작성일: 2025-01-10*  
*작성자: 웹소설나침반 개발팀*  
*버전: v1.0*
# 웹소설나침반 - 마이크로서비스 프로젝트 폴더 구조

## 📁 전체 프로젝트 구조

```
webnovel-compass/
├── microservices/             # 🎯 마이크로서비스들
│   ├── eureka-server/         # 서비스 디스커버리
│   ├── api-gateway/           # API 게이트웨이
│   ├── user-service/          # 사용자 관리 서비스
│   ├── content-service/       # 콘텐츠 관리 서비스
│   ├── analytics-service/     # 분석 서비스
│   └── recommendation-service/ # 추천 서비스 (Python)
├── frontend/                  # React 프론트엔드
├── docker/                    # Docker 관련 파일들
├── database/                  # 데이터베이스 관련
├── docs/                      # 프로젝트 문서
├── scripts/                   # 유틸리티 스크립트
├── config/                    # 설정 파일
├── tests/                     # 통합 테스트
└── README.md                  # 프로젝트 메인 문서
```

## 🏗️ 마이크로서비스별 역할

### `/microservices/eureka-server` - 서비스 디스커버리
- **기술 스택**: Spring Boot + Netflix Eureka
- **포트**: 8761
- **역할**: 
  - 마이크로서비스 등록 및 발견
  - 서비스 상태 모니터링
  - 로드 밸런싱 지원
- **의존성**: 없음 (가장 먼저 실행)

### `/microservices/api-gateway` - API 게이트웨이
- **기술 스택**: Spring Boot + Spring Cloud Gateway
- **포트**: 8080
- **역할**:
  - 클라이언트 요청 라우팅
  - 인증/인가 중앙화
  - Rate Limiting, Circuit Breaker
  - 로깅 및 모니터링
- **의존성**: Eureka Server

### `/microservices/user-service` - 사용자 관리 서비스
- **기술 스택**: Spring Boot + JPA + PostgreSQL
- **포트**: 8081
- **역할**:
  - 사용자 인증/인가 (JWT)
  - 회원가입, 로그인, 프로필 관리
  - 사용자 취향 설정
  - 소셜 로그인 연동
- **데이터베이스**: userdb (PostgreSQL)
- **의존성**: Eureka Server, PostgreSQL

### `/microservices/content-service` - 콘텐츠 관리 서비스
- **기술 스택**: Spring Boot + JPA + Elasticsearch
- **포트**: 8082
- **역할**:
  - 웹소설 메타데이터 관리
  - 평점/리뷰 시스템
  - 검색 및 필터링
  - 콘텐츠 통계 관리
- **데이터베이스**: contentdb (PostgreSQL), Elasticsearch
- **의존성**: Eureka Server, PostgreSQL, Elasticsearch

### `/microservices/analytics-service` - 분석 서비스
- **기술 스택**: Spring Boot + WebFlux + Redis
- **포트**: 8083
- **역할**:
  - 사용자 행동 이벤트 수집 (10ms 이하)
  - 실시간 스트림 처리
  - 세션 관리 및 추적
  - 통계 분석 및 리포팅
- **데이터베이스**: analyticsdb (PostgreSQL), Redis
- **이벤트**: Redis Pub/Sub
- **의존성**: Eureka Server, PostgreSQL, Redis

### `/microservices/recommendation-service` - 추천 서비스
- **기술 스택**: Python + FastAPI + scikit-learn
- **포트**: 8084
- **역할**:
  - AI 추천 알고리즘 (협업/콘텐츠 기반)
  - 개인화 추천 생성
  - 모델 학습 및 업데이트
  - 추천 성능 측정
- **데이터베이스**: PostgreSQL (모델 메타데이터), Redis (캐시)
- **의존성**: PostgreSQL, Redis

## 🔧 인프라 및 지원 폴더

### `/frontend` - React 프론트엔드
- **기술 스택**: React.js + TypeScript
- **역할**:
  - 사용자 인터페이스 (UI/UX)
  - API Gateway를 통한 백엔드 통신
  - 추천 결과 표시 및 상호작용
  - 반응형 웹 디자인

### `/docker` - 컨테이너화
- **파일 구성**:
  ```
  docker/
  ├── docker-compose.yml        # 전체 서비스 오케스트레이션
  ├── docker-compose.dev.yml    # 개발 환경 설정
  ├── postgres-init/            # PostgreSQL 초기화 스크립트
  │   ├── 01-create-databases.sql
  │   └── 02-init-schema.sql
  └── nginx/                    # 프론트엔드 배포용 (선택사항)
      └── nginx.conf
  ```
- **역할**:
  - 단일 명령어로 전체 환경 구성
  - 개발/운영 환경별 설정 분리
  - 네트워크 및 볼륨 관리

### `/database` - 데이터베이스 관련
- **구성**:
  ```
  database/
  ├── migrations/               # DB 마이그레이션 스크립트
  │   ├── user/                # User Service DB
  │   ├── content/             # Content Service DB
  │   └── analytics/           # Analytics Service DB
  ├── seeds/                   # 초기 데이터
  │   ├── sample-users.sql
  │   ├── sample-novels.sql
  │   └── sample-genres.sql
  └── schemas/                 # ERD 및 스키마 문서
      ├── user-service-erd.md
      ├── content-service-erd.md
      └── analytics-service-erd.md
  ```

### `/docs` - 프로젝트 문서
- **구성**:
  ```
  docs/
  ├── architecture/            # 아키텍처 문서
  │   ├── system-overview.md
  │   ├── microservices-design.md
  │   └── data-flow.md
  ├── api/                     # API 문서
  │   ├── user-service-api.md
  │   ├── content-service-api.md
  │   └── analytics-service-api.md
  ├── deployment/              # 배포 가이드
  │   ├── local-setup.md
  │   └── docker-guide.md
  └── requirements/            # 기존 요구사항 명세서들
  ```

### `/scripts` - 유틸리티 스크립트
- **구성**:
  ```
  scripts/
  ├── setup/                   # 환경 설정
  │   ├── setup-dev.sh        # 개발 환경 설정
  │   └── install-deps.sh     # 의존성 설치
  ├── build/                   # 빌드 스크립트
  │   ├── build-all.sh        # 전체 서비스 빌드
  │   └── build-service.sh    # 개별 서비스 빌드
  ├── data/                    # 데이터 관련
  │   ├── import-novels.py    # 웹소설 데이터 수집
  │   └── generate-test-data.py # 테스트 데이터 생성
  └── deploy/                  # 배포 관련
      ├── deploy.sh           # 배포 스크립트
      └── health-check.sh     # 서비스 상태 확인
  ```

### `/config` - 설정 파일
- **구성**:
  ```
  config/
  ├── .env.template            # 환경변수 템플릿
  ├── application-dev.yml      # 개발 환경 공통 설정
  ├── application-prod.yml     # 운영 환경 공통 설정
  └── logging/                 # 로깅 설정
      ├── logback-dev.xml
      └── logback-prod.xml
  ```

### `/tests` - 통합 테스트
- **구성**:
  ```
  tests/
  ├── integration/             # 통합 테스트
  │   ├── user-service-test/
  │   ├── content-service-test/
  │   └── end-to-end-test/
  ├── performance/             # 성능 테스트
  │   ├── load-test/
  │   └── stress-test/
  └── contract/                # 계약 테스트 (Pact)
      ├── user-content-contract/
      └── analytics-recommendation-contract/
  ```

## 🚀 개발 순서

### Phase 1: 기본 인프라 (1-2일)
1. **Eureka Server** - 서비스 디스커버리 구축
2. **API Gateway** - 기본 라우팅 설정
3. **Docker Compose** - 기본 환경 구성

### Phase 2: 핵심 서비스 (3-5일)
4. **User Service** - 인증/사용자 관리
5. **Content Service** - 웹소설 CRUD + 검색
6. **서비스 간 통신** - REST API 연동

### Phase 3: 고급 기능 (5-7일)
7. **Analytics Service** - 이벤트 수집/분석
8. **Recommendation Service** - AI 추천 알고리즘
9. **이벤트 기반 통신** - Redis Pub/Sub

### Phase 4: 통합 및 최적화 (2-3일)
10. **Frontend 연동** - UI 구현
11. **통합 테스트** - E2E 테스트
12. **성능 최적화** - 캐싱, 모니터링

## 📊 리소스 사용량 (단일 서버)

```yaml
메모리 사용량 (총 ~3.3GB):
  - Eureka Server: ~300MB
  - API Gateway: ~400MB
  - User Service: ~500MB
  - Content Service: ~600MB (Elasticsearch 연동)
  - Analytics Service: ~500MB
  - Recommendation Service: ~400MB (Python)
  - PostgreSQL: ~500MB
  - Redis: ~256MB
  - Elasticsearch: ~500MB

포트 사용:
  - API Gateway: 8080 (외부 접근)
  - Eureka Server: 8761
  - User Service: 8081
  - Content Service: 8082
  - Analytics Service: 8083
  - Recommendation Service: 8084
  - PostgreSQL: 5432
  - Redis: 6379
  - Elasticsearch: 9200
```

---

**다음 단계**: `microservices/` 폴더부터 차근차근 생성하여 실제 마이크로서비스 구현을 시작합니다! 🚀
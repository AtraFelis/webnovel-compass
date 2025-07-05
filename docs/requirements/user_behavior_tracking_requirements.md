# 웹소설나침반 - 사용자 행동 추적 시스템 요구사항 명세서

## 문서 정보
- **프로젝트명**: 웹소설나침반 (WebNovel Compass)
- **문서 버전**: 1.0
- **작성일**: 2025-07-04
- **문서 유형**: 사용자 행동 추적 시스템 요구사항 명세서

## 목차
1. [개요](#1-개요)
2. [기능 요구사항](#2-기능-요구사항)
   - 2.1 [행동 데이터 수집](#21-행동-데이터-수집)
   - 2.2 [세션 관리](#22-세션-관리)
   - 2.3 [상호작용 추적](#23-상호작용-추적)
   - 2.4 [검색 행동 분석](#24-검색-행동-분석)
   - 2.5 [추천 효과 측정](#25-추천-효과-측정)
   - 2.6 [데이터 분석 및 처리](#26-데이터-분석-및-처리)
3. [비기능 요구사항](#3-비기능-요구사항)
4. [데이터 요구사항](#4-데이터-요구사항)
5. [보안 및 개인정보 요구사항](#5-보안-및-개인정보-요구사항)
6. [인터페이스 요구사항](#6-인터페이스-요구사항)
7. [제약사항](#7-제약사항)

## 1. 개요

### 1.1 목적
웹소설 추천 플랫폼에서 사용자의 행동 패턴을 체계적으로 수집하고 분석하여 개인화 추천 시스템의 정확도를 향상시키고, 사용자 경험 개선을 위한 인사이트를 제공한다.

### 1.2 범위
- 웹사이트 내 모든 사용자 행동 추적
- 외부 플랫폼으로의 이동 추적  
- 검색 및 필터링 패턴 분석
- 추천 시스템 효과 측정
- 사용자 취향 변화 모니터링

### 1.3 용어 정의
- **행동 이벤트**: 사용자가 수행하는 모든 액션 (클릭, 뷰, 검색 등)
- **세션**: 사용자의 연속된 활동 기간
- **퍼널**: 사용자가 목표 행동에 도달하는 단계별 과정
- **전환율**: 특정 행동에서 목표 행동으로 이어지는 비율

## 2. 기능 요구사항

### 2.1 행동 데이터 수집

#### 2.1.1 페이지뷰 추적 (REQ-TRACK-001)
**기능 설명**: 사용자의 페이지 방문 기록 수집
**수집 데이터**:
- 방문 페이지 URL, 페이지 타입
- 방문 시간, 체류 시간
- 이전 페이지 (referrer)
- 디바이스 정보 (모바일/PC)
- 브라우저 정보
**처리**: 
- 실시간 이벤트 수집
- 중복 방문 필터링 (동일 세션 내 3초 이내 재방문)
**출력**: 페이지뷰 로그 저장

#### 2.1.2 웹소설 조회 추적 (REQ-TRACK-002)
**기능 설명**: 웹소설 상세 페이지 조회 행동 추적
**수집 데이터**:
- 웹소설 ID, 제목
- 조회 시간, 체류 시간
- 스크롤 깊이 (25%, 50%, 75%, 100%)
- 조회 경로 (홈페이지, 검색, 추천 등)
- 이후 행동 (북마크, 외부 링크 클릭 등)
**처리**: 스크롤 이벤트를 통한 관심도 측정

#### 2.1.3 외부 링크 클릭 추적 (REQ-TRACK-003)
**기능 설명**: 외부 웹소설 플랫폼으로의 이동 추적
**수집 데이터**:
- 웹소설 ID, 외부 플랫폼명
- 클릭 시간, 클릭 위치
- 추천 알고리즘 정보 (해당 시)
**처리**: 
- 실제 전환 행동으로 간주 (높은 가중치)
- 추천 효과 측정에 활용
**출력**: 전환 이벤트 로그

### 2.2 세션 관리

#### 2.2.1 세션 생성 및 관리 (REQ-SESSION-001)
**기능 설명**: 사용자 세션 생성 및 추적
**세션 정의**: 30분 비활성 시 세션 종료
**수집 데이터**:
- 세션 ID, 사용자 ID (로그인 시)
- 세션 시작/종료 시간
- 총 페이지뷰 수, 체류 시간
- 접속 경로 (직접, 검색엔진, 추천 등)
- IP 주소 (해시 처리), User-Agent
**처리**: Redis를 통한 실시간 세션 상태 관리

#### 2.2.2 익명 사용자 추적 (REQ-SESSION-002)
**기능 설명**: 비로그인 사용자의 행동 추적
**처리**:
- 브라우저 쿠키 기반 임시 ID 생성
- 로그인 시 기존 익명 데이터와 연결
- 개인정보 보호 정책 준수
**제한사항**: 쿠키 동의 사용자만 추적

### 2.3 상호작용 추적

#### 2.3.1 북마크/찜하기 추적 (REQ-INTERACT-001)
**기능 설명**: 사용자의 관심 표현 행동 추적
**수집 데이터**:
- 웹소설 ID, 액션 타입 (북마크, 찜하기, 취소)
- 액션 시간, 액션 위치
- 이후 행동 연계 분석
**처리**: 명시적 선호도로 높은 가중치 부여

#### 2.3.2 평점/리뷰 행동 추적 (REQ-INTERACT-002)
**기능 설명**: 평가 행동과 관련된 상세 추적
**수집 데이터**:
- 평점 입력 과정 (수정 횟수, 고민 시간)
- 리뷰 작성 시간, 길이
- 평점/리뷰 조회 행동
**처리**: 신뢰도 높은 피드백으로 분류

#### 2.3.3 공유 행동 추적 (REQ-INTERACT-003)
**기능 설명**: 웹소설 공유 및 추천 행동 추적
**수집 데이터**:
- 공유 플랫폼 (SNS, 메신저 등)
- 공유된 웹소설 정보
- 공유 후 반응 (가능한 경우)

### 2.4 검색 행동 분석

#### 2.4.1 검색어 추적 (REQ-SEARCH-001)
**기능 설명**: 사용자 검색 패턴 분석
**수집 데이터**:
- 검색어, 검색 시간
- 검색 결과 수, 클릭된 결과
- 검색 후 행동 패턴
- 검색어 수정/보완 과정
**처리**: 
- 검색 의도 분석 (작가명, 제목, 장르 등)
- 개인화 검색 개선에 활용

#### 2.4.2 필터링 패턴 추적 (REQ-SEARCH-002)
**기능 설명**: 검색 필터 사용 패턴 분석
**수집 데이터**:
- 사용된 필터 조합 (장르, 상태, 평점 등)
- 필터 적용 순서
- 필터 결과에 대한 만족도 (클릭률)
**처리**: 개인화 필터 추천에 활용

#### 2.4.3 자동완성 상호작용 (REQ-SEARCH-003)
**기능 설명**: 검색 자동완성 사용 패턴 추적
**수집 데이터**:
- 자동완성 후보 선택/무시
- 타이핑 vs 선택 비율
- 자동완성 만족도

### 2.5 추천 효과 측정

#### 2.5.1 추천 노출 추적 (REQ-RECOMMEND-001)
**기능 설명**: 추천 시스템 성능 측정을 위한 노출 추적
**수집 데이터**:
- 추천 알고리즘 ID, 버전
- 추천된 웹소설 목록 (순서 포함)
- 노출 위치 (홈페이지, 상세페이지 등)
- 노출 시간, 화면 체류 시간
**처리**: A/B 테스트 기반 성능 비교

#### 2.5.2 추천 클릭 추적 (REQ-RECOMMEND-002)
**기능 설명**: 추천 항목에 대한 사용자 반응 추적
**수집 데이터**:
- 클릭된 추천 항목 순위
- 클릭까지의 시간
- 클릭 후 행동 (체류시간, 전환 여부)
**처리**: 
- 추천 성능 지표 계산 (CTR, 전환율)
- 실시간 추천 품질 모니터링

#### 2.5.3 추천 피드백 추적 (REQ-RECOMMEND-003)
**기능 설명**: 명시적 추천 피드백 수집
**수집 데이터**:
- 좋아요/싫어요 버튼 클릭
- "관심 없음" 선택 이유
- 추천 개선 요청 사항
**처리**: 즉시 개인화 모델에 반영

### 2.6 데이터 분석 및 처리

#### 2.6.1 실시간 분석 (REQ-ANALYSIS-001)
**기능 설명**: 실시간 사용자 행동 분석
**분석 내용**:
- 현재 세션 내 관심 패턴 감지
- 이상 행동 탐지 (봇, 크롤러)
- 실시간 개인화 업데이트
**처리 주기**: 이벤트 발생 즉시

#### 2.6.2 배치 분석 (REQ-ANALYSIS-002)
**기능 설명**: 주기적 행동 패턴 분석
**분석 내용**:
- 일별/주별 사용자 행동 트렌드
- 취향 변화 패턴 감지
- 코호트 분석 (가입 시기별 행동 비교)
**처리 주기**: 일 1회 (새벽 2시)

#### 2.6.3 사용자 프로필 업데이트 (REQ-ANALYSIS-003)
**기능 설명**: 행동 데이터 기반 사용자 프로필 자동 업데이트
**업데이트 요소**:
- 장르 선호도 가중치 조정
- 새로운 관심 태그 발견
- 활동 패턴 변화 반영
**처리**: 점진적 학습을 통한 부드러운 업데이트

## 3. 비기능 요구사항

### 3.1 성능 요구사항
- **이벤트 수집**: 평균 10ms 이하, 99% 요청 50ms 이하
- **동시 처리**: 초당 10,000개 이벤트 처리 가능
- **데이터 지연**: 실시간 분석 1초 이하, 배치 분석 24시간 이내
- **저장소 성능**: 일일 1억 건 이벤트 저장 가능

### 3.2 확장성 요구사항
- **사용자 확장**: 동시 접속자 10만 명 지원
- **데이터 증가**: 월 100TB 데이터 증가 대응
- **분산 처리**: 여러 서버로 부하 분산 가능
- **실시간 스트림**: Apache Kafka 기반 확장 가능

### 3.3 가용성 요구사항
- **시스템 가용성**: 99.9% 이상
- **데이터 유실**: 0.01% 이하 (중요 이벤트는 0%)
- **복구 시간**: 장애 시 10분 이내 복구
- **백업**: 실시간 복제 + 일일 백업

## 4. 데이터 요구사항

### 4.1 사용자 행동 이벤트 테이블
```sql
user_behavior_events (
    event_id BIGINT PRIMARY KEY,
    user_id BIGINT, -- NULL for anonymous users
    session_id VARCHAR(100) NOT NULL,
    event_type VARCHAR(50) NOT NULL, -- 'PAGE_VIEW', 'CLICK', 'SEARCH', 'BOOKMARK', etc.
    event_category VARCHAR(30), -- 'NAVIGATION', 'INTERACTION', 'CONVERSION'
    target_type VARCHAR(30), -- 'NOVEL', 'AUTHOR', 'SEARCH_RESULT', etc.
    target_id BIGINT, -- Novel ID, Author ID, etc.
    event_data JSON, -- Additional event-specific data
    page_url VARCHAR(500),
    referrer_url VARCHAR(500),
    user_agent TEXT,
    ip_hash VARCHAR(64), -- Hashed IP for privacy
    device_type ENUM('MOBILE', 'TABLET', 'DESKTOP'),
    created_at TIMESTAMP DEFAULT NOW(),
    processed_at TIMESTAMP,
    
    INDEX idx_user_created (user_id, created_at),
    INDEX idx_session_created (session_id, created_at),
    INDEX idx_event_type_created (event_type, created_at),
    INDEX idx_target (target_type, target_id)
)
```

### 4.2 사용자 세션 테이블
```sql
user_sessions (
    session_id VARCHAR(100) PRIMARY KEY,
    user_id BIGINT,
    started_at TIMESTAMP NOT NULL,
    ended_at TIMESTAMP,
    total_page_views INT DEFAULT 0,
    total_duration_seconds INT DEFAULT 0,
    entry_page VARCHAR(500),
    exit_page VARCHAR(500),
    traffic_source VARCHAR(100), -- 'DIRECT', 'SEARCH', 'SOCIAL', etc.
    campaign_source VARCHAR(100), -- UTM tracking
    device_info JSON,
    location_info JSON, -- City, Country (if available)
    is_bounce BOOLEAN DEFAULT FALSE,
    conversion_events INT DEFAULT 0, -- Number of conversion events
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_user_started (user_id, started_at),
    INDEX idx_started_at (started_at),
    INDEX idx_traffic_source (traffic_source)
)
```

### 4.3 웹소설 조회 로그 테이블
```sql
novel_view_logs (
    log_id BIGINT PRIMARY KEY,
    user_id BIGINT,
    session_id VARCHAR(100) NOT NULL,
    novel_id BIGINT NOT NULL,
    view_started_at TIMESTAMP NOT NULL,
    view_duration_seconds INT,
    scroll_depth DECIMAL(5,2), -- Max scroll percentage
    came_from VARCHAR(100), -- 'HOMEPAGE', 'SEARCH', 'RECOMMENDATION', etc.
    recommendation_context JSON, -- If from recommendation
    actions_taken JSON, -- ['BOOKMARK', 'EXTERNAL_CLICK', 'RATING']
    exit_action VARCHAR(50), -- Last action before leaving
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_user_novel (user_id, novel_id),
    INDEX idx_novel_created (novel_id, created_at),
    INDEX idx_session_created (session_id, created_at),
    FOREIGN KEY (novel_id) REFERENCES novels(novel_id)
)
```

### 4.4 검색 행동 로그 테이블
```sql
search_behavior_logs (
    search_id BIGINT PRIMARY KEY,
    user_id BIGINT,
    session_id VARCHAR(100) NOT NULL,
    search_query VARCHAR(500) NOT NULL,
    search_filters JSON, -- Applied filters
    result_count INT,
    clicked_results JSON, -- [{"novel_id": 123, "position": 1, "clicked_at": "..."}]
    search_duration_seconds INT,
    refined_to VARCHAR(500), -- If query was refined
    search_intent VARCHAR(50), -- 'TITLE', 'AUTHOR', 'GENRE', 'MIXED'
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_user_created (user_id, created_at),
    INDEX idx_session_created (session_id, created_at),
    INDEX idx_query (search_query(100)),
    INDEX idx_created_at (created_at)
)
```

### 4.5 추천 효과 측정 테이블
```sql
recommendation_tracking (
    tracking_id BIGINT PRIMARY KEY,
    user_id BIGINT,
    session_id VARCHAR(100) NOT NULL,
    recommendation_context VARCHAR(100), -- 'HOMEPAGE', 'NOVEL_DETAIL', etc.
    algorithm_name VARCHAR(50),
    algorithm_version VARCHAR(20),
    recommended_novels JSON, -- [{"novel_id": 123, "position": 1, "score": 0.95}]
    exposed_at TIMESTAMP NOT NULL,
    interaction_events JSON, -- Clicks, views, etc.
    conversion_events JSON, -- External clicks, bookmarks
    feedback_score DECIMAL(3,2), -- If explicit feedback given
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_user_exposed (user_id, exposed_at),
    INDEX idx_algorithm (algorithm_name, algorithm_version),
    INDEX idx_context_exposed (recommendation_context, exposed_at)
)
```

## 5. 보안 및 개인정보 요구사항

### 5.1 개인정보 보호
- **데이터 최소화**: 추천 개선에 필요한 최소한의 데이터만 수집
- **익명화 처리**: IP 주소 해시 처리, 식별 가능한 정보 제거
- **동의 기반 수집**: 쿠키 동의 및 추적 동의 관리
- **삭제 요청 처리**: 사용자 요청 시 개인 행동 데이터 완전 삭제

### 5.2 데이터 보안
- **전송 보안**: HTTPS를 통한 모든 데이터 전송
- **저장 보안**: 민감 데이터 암호화 저장
- **접근 제어**: 역할 기반 데이터 접근 제한
- **감사 로그**: 모든 데이터 접근 및 수정 기록

### 5.3 개인정보 보관 정책
- **활성 사용자**: 최근 2년간 활동 기록 보관
- **비활성 사용자**: 1년 후 개인 식별 정보 삭제, 익명화 데이터만 보관
- **탈퇴 사용자**: 30일 후 모든 개인 데이터 완전 삭제
- **법적 요구**: 관련 법령에 따른 최소 보관 기간 준수

## 6. 인터페이스 요구사항

### 6.1 이벤트 수집 API
```javascript
// 클라이언트 사이드 추적 API
POST /api/v1/tracking/events
{
  "event_type": "PAGE_VIEW",
  "event_category": "NAVIGATION", 
  "target_type": "NOVEL",
  "target_id": 12345,
  "event_data": {
    "scroll_depth": 0.75,
    "time_spent": 45
  },
  "page_url": "/novels/12345",
  "referrer": "/search?q=fantasy"
}

// 배치 이벤트 전송
POST /api/v1/tracking/events/batch
{
  "session_id": "sess_abc123",
  "events": [...]
}
```

### 6.2 분석 데이터 조회 API
```javascript
// 사용자 행동 분석 조회 (내부 API)
GET /api/v1/analytics/user/{user_id}/behavior
GET /api/v1/analytics/user/{user_id}/preferences  
GET /api/v1/analytics/novel/{novel_id}/interactions
GET /api/v1/analytics/recommendations/performance

// 실시간 통계
GET /api/v1/analytics/realtime/active-users
GET /api/v1/analytics/realtime/popular-novels
```

### 6.3 외부 시스템 연동
- **추천 시스템**: 행동 데이터 실시간 스트리밍 (Kafka)
- **분석 시스템**: 배치 데이터 전송 (S3, BigQuery)
- **모니터링**: 실시간 메트릭 전송 (Prometheus)
- **A/B 테스트**: 실험 결과 데이터 연동

## 7. 제약사항

### 7.1 기술적 제약사항
- **이벤트 큐**: Redis Streams 또는 Apache Kafka 사용
- **대용량 저장**: PostgreSQL + 시계열 DB (InfluxDB) 조합
- **실시간 처리**: Spring Boot WebFlux 사용
- **배치 처리**: Spring Batch 또는 Apache Spark

### 7.2 법적 제약사항
- **개인정보보호법**: 국내 개인정보 보호 규정 준수
- **GDPR**: EU 사용자 대상 서비스 시 적용
- **쿠키 정책**: 필수/선택 쿠키 구분 및 동의 관리
- **아동 보호**: 만 14세 미만 개인정보 수집 제한

### 7.3 비즈니스 제약사항
- **사용자 경험**: 추적 기능이 서비스 성능에 영향을 주지 않아야 함
- **투명성**: 사용자가 데이터 수집 현황을 확인할 수 있어야 함
- **선택권**: 추적 거부 시에도 기본 서비스 이용 가능해야 함
- **데이터 활용**: 수집된 데이터는 서비스 개선 목적으로만 사용

### 7.4 운영 제약사항
- **데이터 보관**: 스토리지 비용 고려한 데이터 보관 정책
- **처리 성능**: 실시간 처리 지연으로 인한 사용자 경험 저하 방지
- **모니터링**: 24시간 실시간 시스템 상태 모니터링 필요
- **장애 대응**: 데이터 유실 방지를 위한 다중화 및 백업 체계

## 부록

### A. 이벤트 타입 정의
```javascript
// 주요 이벤트 타입
EVENT_TYPES = {
  // 네비게이션
  'PAGE_VIEW': '페이지 조회',
  'PAGE_EXIT': '페이지 이탈',
  
  // 상호작용
  'CLICK': '클릭',
  'SCROLL': '스크롤',
  'HOVER': '마우스 오버',
  
  // 웹소설 관련
  'NOVEL_VIEW': '웹소설 조회',
  'NOVEL_BOOKMARK': '북마크 추가/제거',
  'EXTERNAL_CLICK': '외부 링크 클릭',
  
  // 검색
  'SEARCH': '검색 실행',
  'SEARCH_FILTER': '필터 적용',
  'AUTOCOMPLETE_SELECT': '자동완성 선택',
  
  // 추천
  'RECOMMENDATION_VIEW': '추천 노출',
  'RECOMMENDATION_CLICK': '추천 클릭',
  'RECOMMENDATION_FEEDBACK': '추천 피드백',
  
  // 평가
  'RATING': '평점 입력',
  'REVIEW': '리뷰 작성',
  
  // 계정
  'LOGIN': '로그인',
  'LOGOUT': '로그아웃',
  'SIGNUP': '회원가입'
}
```

### B. 개인정보 처리 방침 고려사항
1. **수집하는 개인정보**
   - 서비스 이용 기록 (접속 로그, 이용 기록 등)
   - 쿠키, 접속 IP 정보 등

2. **개인정보 수집 목적**
   - 개인화 서비스 제공
   - 서비스 이용 통계 분석
   - 서비스 개선 및 품질 향상

3. **개인정보 보유 기간**
   - 서비스 이용 기록: 1년 (법정 보관 의무 제외)
   - 접속 로그: 3개월

### C. 성능 모니터링 지표
- **수집 성능**: 초당 이벤트 처리량, 응답 시간
- **저장 성능**: 데이터베이스 write 성능, 디스크 사용량
- **분석 성능**: 실시간 분석 지연 시간, 배치 처리 시간
- **서비스 영향**: 웹사이트 로딩 속도에 미치는 영향
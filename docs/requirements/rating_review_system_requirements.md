# 웹소설나침반 - 평점 및 리뷰 시스템 요구사항 명세서

## 문서 정보
- **프로젝트명**: 웹소설나침반 (WebNovel Compass)
- **문서 버전**: 1.0
- **작성일**: 2025-07-04
- **문서 유형**: 평점 및 리뷰 시스템 요구사항 명세서

## 목차
1. [개요](#1-개요)
2. [기능 요구사항](#2-기능-요구사항)
   - 2.1 [평점 시스템](#21-평점-시스템)
   - 2.2 [리뷰 시스템](#22-리뷰-시스템)
   - 2.3 [스포일러 관리](#23-스포일러-관리)
   - 2.4 [리뷰 상호작용](#24-리뷰-상호작용)
   - 2.5 [신뢰도 관리](#25-신뢰도-관리)
   - 2.6 [통계 및 분석](#26-통계-및-분석)
   - 2.7 [관리 및 모더레이션](#27-관리-및-모더레이션)
3. [비기능 요구사항](#3-비기능-요구사항)
4. [데이터 요구사항](#4-데이터-요구사항)
5. [보안 요구사항](#5-보안-요구사항)
6. [인터페이스 요구사항](#6-인터페이스-요구사항)
7. [제약사항](#7-제약사항)

## 1. 개요

### 1.1 목적
웹소설 추천 플랫폼에서 사용자들이 웹소설에 대한 평가와 의견을 공유할 수 있는 시스템을 구축하여, 다른 사용자들의 작품 선택에 도움을 주고 추천 시스템의 정확도를 향상시킨다.

### 1.2 범위
- 1-5점 평점 시스템
- 텍스트 리뷰 작성 및 관리
- 스포일러 탐지 및 관리
- 리뷰 유용성 평가 시스템
- 사용자 신뢰도 관리
- 부적절한 콘텐츠 신고 및 처리

### 1.3 용어 정의
- **평점**: 1-5점 척도의 숫자 평가
- **리뷰**: 웹소설에 대한 텍스트 평가 및 의견
- **스포일러**: 작품의 핵심 내용을 미리 공개하는 정보
- **신뢰도**: 사용자의 평가 신뢰성을 나타내는 지수
- **유용성**: 다른 사용자들이 해당 리뷰가 도움되었는지 평가하는 지표

## 2. 기능 요구사항

### 2.1 평점 시스템

#### 2.1.1 평점 등록 (REQ-RATING-001)
**기능 설명**: 웹소설에 대한 1-5점 평점 등록
**입력**: 사용자 ID, 웹소설 ID, 평점 (1-5점)
**처리**:
- 사용자당 웹소설별 1개 평점만 허용
- 기존 평점 수정 가능 (이력 보관)
- 실시간 평균 평점 업데이트
- 추천 시스템 피드백 전송
**출력**: 평점 등록 성공/실패, 업데이트된 평균 평점
**예외처리**: 중복 평점, 잘못된 범위, 존재하지 않는 웹소설

#### 2.1.2 평점 조회 (REQ-RATING-002)
**기능 설명**: 웹소설의 평점 통계 조회
**입력**: 웹소설 ID
**출력**: 
- 평균 평점 (소수점 2자리)
- 평점 분포 (1-5점별 개수)
- 총 평점 참여자 수
- 최근 30일 평점 동향
**성능**: 100ms 이하 응답 시간

#### 2.1.3 평점 수정/삭제 (REQ-RATING-003)
**기능 설명**: 사용자 평점 수정 또는 삭제
**입력**: 평점 ID, 새로운 평점 또는 삭제 요청
**처리**:
- 평점 변경 이력 기록
- 평균 평점 재계산
- 통계 데이터 업데이트
**제한사항**: 평점 등록 후 24시간 내에만 수정 가능

### 2.2 리뷰 시스템

#### 2.2.1 리뷰 작성 (REQ-REVIEW-001)
**기능 설명**: 웹소설에 대한 텍스트 리뷰 작성
**입력**: 
- 사용자 ID, 웹소설 ID
- 리뷰 제목 (100자 이내)
- 리뷰 내용 (3,000자 이내)
- 스포일러 포함 여부
- 추천 여부 (추천/보통/비추천)
**처리**:
- 욕설/부적절한 표현 자동 필터링
- 스포일러 자동 탐지 (AI 기반)
- 중복 리뷰 검사 (동일 사용자)
**출력**: 리뷰 등록 성공/실패, 리뷰 ID
**예외처리**: 글자 수 초과, 부적절한 내용, 중복 리뷰

#### 2.2.2 리뷰 조회 (REQ-REVIEW-002)
**기능 설명**: 웹소설 리뷰 목록 조회
**입력**: 웹소설 ID, 정렬 기준, 페이지 정보
**정렬 옵션**:
- 최신순, 오래된순
- 유용성 높은 순
- 평점 높은 순, 낮은 순
**필터 옵션**:
- 스포일러 포함/제외
- 평점 범위 (예: 4-5점만)
- 리뷰 길이 (상세/간단)
**출력**: 페이지네이션된 리뷰 목록

#### 2.2.3 리뷰 수정 (REQ-REVIEW-003)
**기능 설명**: 작성한 리뷰 수정
**입력**: 리뷰 ID, 수정할 내용
**처리**:
- 수정 이력 보관 (최대 5개 버전)
- 재검토 대상으로 분류
- 수정 시간 기록
**제한사항**: 
- 리뷰 작성자만 수정 가능
- 리뷰 작성 후 7일 내에만 수정 가능

#### 2.2.4 리뷰 삭제 (REQ-REVIEW-004)
**기능 설명**: 리뷰 삭제 (논리 삭제)
**처리**:
- 논리 삭제 (is_deleted = true)
- 통계에서 제외
- 30일 후 물리 삭제
**권한**: 작성자 본인 또는 관리자

### 2.3 스포일러 관리

#### 2.3.1 스포일러 자동 탐지 (REQ-SPOILER-001)
**기능 설명**: AI 기반 스포일러 내용 자동 탐지
**탐지 대상**:
- 결말 관련 키워드
- 주요 사건 공개
- 캐릭터 운명 관련 내용
**처리**:
- 자연어 처리를 통한 내용 분석
- 키워드 매칭 및 문맥 분석
- 의심 스포일러 표시 및 사용자 확인 요청
**정확도 목표**: 90% 이상

#### 2.3.2 스포일러 표시 및 필터링 (REQ-SPOILER-002)
**기능 설명**: 스포일러 내용 표시 방식 관리
**표시 방식**:
- 스포일러 경고 문구 표시
- 내용 블러 처리 또는 접기
- 클릭 시에만 내용 표시
**사용자 설정**:
- 스포일러 자동 숨김 설정
- 완결작은 스포일러 허용 설정
- 특정 장르 스포일러 민감도 설정

#### 2.3.3 스포일러 신고 처리 (REQ-SPOILER-003)
**기능 설명**: 사용자 신고를 통한 스포일러 관리
**신고 처리**:
- 신고 접수 및 검토 대기열 추가
- 관리자 검토 및 판정
- 판정 결과에 따른 조치 (경고, 삭제 등)
**자동 조치**: 동일 리뷰에 스포일러 신고 5건 이상 시 임시 숨김

### 2.4 리뷰 상호작용

#### 2.4.1 리뷰 유용성 평가 (REQ-HELPFUL-001)
**기능 설명**: 리뷰가 도움되었는지 평가
**평가 옵션**:
- 도움됨 / 도움안됨
- 재미있음 / 재미없음
- 공감됨 / 공감안됨
**처리**:
- 사용자당 리뷰별 1회만 평가 가능
- 평가 변경 가능
- 리뷰 점수 실시간 업데이트
**출력**: 유용성 점수, 평가 개수

#### 2.4.2 리뷰 댓글 시스템 (REQ-COMMENT-001)
**기능 설명**: 리뷰에 대한 댓글 작성 및 관리
**기본 기능**:
- 댓글 작성 (500자 이내)
- 댓글 수정/삭제 (작성자만)
- 댓글에 대한 답글 (1단계 깊이만)
**처리**:
- 부적절한 내용 자동 필터링
- 스팸 댓글 탐지 및 차단
**제한사항**: 리뷰당 최대 100개 댓글

#### 2.4.3 리뷰 공유 (REQ-SHARE-001)
**기능 설명**: 우수 리뷰 공유 기능
**공유 방식**:
- SNS 공유 (페이스북, 트위터, 카카오톡)
- 링크 복사
- 이미지 카드 생성
**공유 추적**: 공유 횟수 및 유입 경로 분석

### 2.5 신뢰도 관리

#### 2.5.1 사용자 신뢰도 계산 (REQ-TRUST-001)
**기능 설명**: 사용자의 평가 신뢰도 계산
**계산 요소**:
- 계정 생성 일수 (10%)
- 평점/리뷰 참여 횟수 (20%)
- 리뷰 유용성 평가 받은 정도 (30%)
- 신고 당한 횟수 (역가중치, 20%)
- 일관성 있는 평가 패턴 (20%)
**신뢰도 등급**: 
- 신규 (0-2), 일반 (3-5), 신뢰 (6-8), 전문 (9-10)
**업데이트**: 주 1회 재계산

#### 2.5.2 가중 평점 시스템 (REQ-TRUST-002)
**기능 설명**: 사용자 신뢰도를 반영한 가중 평점 계산
**가중치 적용**:
- 신뢰도 0-2: 가중치 0.5
- 신뢰도 3-5: 가중치 1.0
- 신뢰도 6-8: 가중치 1.5
- 신뢰도 9-10: 가중치 2.0
**표시**: 일반 평점과 가중 평점 모두 표시

#### 2.5.3 이상 패턴 탐지 (REQ-ANOMALY-001)
**기능 설명**: 부정한 평가 패턴 탐지
**탐지 패턴**:
- 단시간 내 대량 평점 등록
- 특정 작가/장르에만 극단적 평점
- 동일 IP에서 여러 계정 평가
- 평점과 리뷰 내용의 불일치
**자동 조치**: 의심 계정 플래그 및 관리자 검토 요청

### 2.6 통계 및 분석

#### 2.6.1 평점 통계 분석 (REQ-STATS-001)
**기능 설명**: 웹소설별 평점 통계 분석
**분석 내용**:
- 시간대별 평점 변화 추이
- 사용자 신뢰도별 평점 분포
- 장르별 평점 경향
- 연재 상태별 평점 차이
**갱신 주기**: 일 1회

#### 2.6.2 리뷰 텍스트 분석 (REQ-STATS-002)
**기능 설명**: 리뷰 내용 텍스트 마이닝
**분석 기능**:
- 자주 언급되는 키워드 추출
- 감정 분석 (긍정/중립/부정)
- 주요 토픽 모델링
- 작품별 특징 키워드
**활용**: 추천 시스템 콘텐츠 기반 필터링에 활용

#### 2.6.3 사용자 취향 분석 (REQ-STATS-003)
**기능 설명**: 사용자별 평가 패턴 분석
**분석 항목**:
- 선호 장르 비율
- 평점 패턴 (관대함/엄격함)
- 리뷰 작성 스타일
- 시간대별 활동 패턴
**개인화**: 분석 결과를 추천 알고리즘에 피드백

### 2.7 관리 및 모더레이션

#### 2.7.1 리뷰 신고 처리 (REQ-MODERATION-001)
**기능 설명**: 부적절한 리뷰 신고 및 처리
**신고 유형**:
- 스포일러 포함
- 욕설/비방
- 무관한 내용
- 광고/스팸
- 허위 리뷰
**처리 프로세스**:
1. 신고 접수 및 자동 분류
2. 관리자 검토 (48시간 내)
3. 조치 결정 (삭제, 경고, 무조치)
4. 신고자 및 작성자 알림

#### 2.7.2 자동 필터링 (REQ-MODERATION-002)
**기능 설명**: AI 기반 부적절한 내용 자동 필터링
**필터링 대상**:
- 욕설 및 비속어
- 개인정보 포함 내용
- 외부 링크 및 광고
- 반복 문자/숫자 스팸
**처리**: 
- 경고 메시지 표시 및 수정 요청
- 심각한 경우 자동 차단
- 관리자 검토 대기열 추가

#### 2.7.3 관리자 도구 (REQ-MODERATION-003)
**기능 설명**: 관리자용 리뷰/평점 관리 도구
**관리 기능**:
- 신고된 리뷰 일괄 처리
- 사용자별 평가 이력 조회
- 평점 조작 의심 사례 분석
- 통계 대시보드
**권한**: 관리자 등급별 차등 권한 부여

## 3. 비기능 요구사항

### 3.1 성능 요구사항
- **평점 등록**: 평균 50ms 이하
- **리뷰 조회**: 페이지당 100ms 이하
- **검색 성능**: 키워드 검색 200ms 이하
- **동시 처리**: 초당 1,000건 평점/리뷰 처리

### 3.2 확장성 요구사항
- **데이터 규모**: 1억 개 평점, 1천만 개 리뷰 지원
- **사용자 증가**: 백만 명 동시 이용자 대응
- **텍스트 분석**: 대용량 리뷰 데이터 실시간 처리
- **국제화**: 다국어 리뷰 지원 구조

### 3.3 가용성 요구사항
- **시스템 가용성**: 99.9% 이상
- **데이터 백업**: 실시간 복제 + 일일 백업
- **장애 복구**: 30분 이내 서비스 복구
- **다운그레이드**: 장애 시 읽기 전용 모드 지원

## 4. 데이터 요구사항

### 4.1 평점 테이블
```sql
user_ratings (
    rating_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    novel_id BIGINT NOT NULL,
    rating DECIMAL(2,1) NOT NULL CHECK (rating >= 1.0 AND rating <= 5.0),
    previous_rating DECIMAL(2,1), -- 이전 평점 (수정 시)
    trust_weight DECIMAL(3,2) DEFAULT 1.0, -- 신뢰도 가중치
    rated_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    ip_hash VARCHAR(64), -- 조작 방지용
    
    UNIQUE KEY unique_user_novel (user_id, novel_id),
    INDEX idx_novel_rating (novel_id, rating),
    INDEX idx_user_rated (user_id, rated_at),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (novel_id) REFERENCES novels(novel_id)
)
```

### 4.2 리뷰 테이블
```sql
user_reviews (
    review_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    novel_id BIGINT NOT NULL,
    title VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    recommendation ENUM('RECOMMEND', 'NEUTRAL', 'NOT_RECOMMEND') DEFAULT 'NEUTRAL',
    has_spoiler BOOLEAN DEFAULT FALSE,
    spoiler_auto_detected BOOLEAN DEFAULT FALSE,
    word_count INT,
    helpful_count INT DEFAULT 0,
    not_helpful_count INT DEFAULT 0,
    comment_count INT DEFAULT 0,
    report_count INT DEFAULT 0,
    view_count INT DEFAULT 0,
    status ENUM('ACTIVE', 'HIDDEN', 'DELETED', 'UNDER_REVIEW') DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    reviewed_version INT DEFAULT 1, -- 수정 버전
    
    INDEX idx_novel_status_helpful (novel_id, status, helpful_count DESC),
    INDEX idx_user_created (user_id, created_at),
    INDEX idx_created_status (created_at, status),
    FULLTEXT INDEX ft_title_content (title, content),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (novel_id) REFERENCES novels(novel_id)
)
```

### 4.3 리뷰 유용성 평가 테이블
```sql
review_helpfulness (
    helpfulness_id BIGINT PRIMARY KEY,
    review_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    is_helpful BOOLEAN NOT NULL, -- true: 도움됨, false: 도움안됨
    feedback_type ENUM('HELPFUL', 'FUNNY', 'AGREE') DEFAULT 'HELPFUL',
    created_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE KEY unique_user_review (user_id, review_id),
    INDEX idx_review_helpful (review_id, is_helpful),
    INDEX idx_user_created (user_id, created_at),
    FOREIGN KEY (review_id) REFERENCES user_reviews(review_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
```

### 4.4 리뷰 댓글 테이블
```sql
review_comments (
    comment_id BIGINT PRIMARY KEY,
    review_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    parent_comment_id BIGINT, -- 답글인 경우
    content VARCHAR(500) NOT NULL,
    status ENUM('ACTIVE', 'HIDDEN', 'DELETED') DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_review_status_created (review_id, status, created_at),
    INDEX idx_user_created (user_id, created_at),
    INDEX idx_parent (parent_comment_id),
    FOREIGN KEY (review_id) REFERENCES user_reviews(review_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (parent_comment_id) REFERENCES review_comments(comment_id)
)
```

### 4.5 사용자 신뢰도 테이블
```sql
user_trust_scores (
    user_id BIGINT PRIMARY KEY,
    trust_score DECIMAL(4,2) DEFAULT 5.0, -- 0.00 ~ 10.00
    trust_level ENUM('NEW', 'BASIC', 'TRUSTED', 'EXPERT') DEFAULT 'NEW',
    total_ratings INT DEFAULT 0,
    total_reviews INT DEFAULT 0,
    helpful_reviews_count INT DEFAULT 0,
    reported_count INT DEFAULT 0,
    account_age_days INT DEFAULT 0,
    consistency_score DECIMAL(3,2) DEFAULT 1.0, -- 일관성 점수
    last_calculated_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_trust_score (trust_score DESC),
    INDEX idx_trust_level (trust_level),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
```

### 4.6 신고 및 모더레이션 테이블
```sql
review_reports (
    report_id BIGINT PRIMARY KEY,
    review_id BIGINT NOT NULL,
    reporter_user_id BIGINT NOT NULL,
    report_type ENUM('SPOILER', 'ABUSE', 'SPAM', 'IRRELEVANT', 'FAKE') NOT NULL,
    report_reason TEXT,
    status ENUM('PENDING', 'REVIEWED', 'RESOLVED', 'REJECTED') DEFAULT 'PENDING',
    moderator_id BIGINT,
    moderator_action ENUM('NO_ACTION', 'WARNING', 'HIDE_REVIEW', 'DELETE_REVIEW', 'BAN_USER'),
    moderator_notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    resolved_at TIMESTAMP,
    
    INDEX idx_status_created (status, created_at),
    INDEX idx_review_type (review_id, report_type),
    INDEX idx_reporter (reporter_user_id),
    FOREIGN KEY (review_id) REFERENCES user_reviews(review_id),
    FOREIGN KEY (reporter_user_id) REFERENCES users(user_id),
    FOREIGN KEY (moderator_id) REFERENCES users(user_id)
)
```

## 5. 보안 요구사항

### 5.1 데이터 무결성
- **중복 방지**: 사용자당 웹소설별 평점 1개, 리뷰 1개 제한
- **조작 방지**: IP 기반 대량 평점 탐지, 패턴 분석
- **데이터 검증**: 입력값 범위 검증, SQL 인젝션 방지
- **무결성 검사**: 정기적인 데이터 일관성 검증

### 5.2 스팸 및 어뷰징 방지
- **속도 제한**: 사용자당 분당 평점 3개, 리뷰 1개 제한
- **봇 탐지**: CAPTCHA, 행동 패턴 분석
- **IP 추적**: 동일 IP에서 다중 계정 평가 탐지
- **텍스트 분석**: 복사/붙여넣기 리뷰 탐지

### 5.3 개인정보 보호
- **익명화**: 신고 처리 시 개인정보 익명화
- **데이터 보관**: 삭제된 리뷰 30일 후 완전 삭제
- **접근 제어**: 관리자 등급별 데이터 접근 권한
- **감사 로그**: 모든 관리 작업 로깅

## 6. 인터페이스 요구사항

### 6.1 평점/리뷰 API
```javascript
// 평점 등록/수정
POST /api/v1/novels/{novel_id}/rating
PUT  /api/v1/ratings/{rating_id}
GET  /api/v1/novels/{novel_id}/ratings/stats

// 리뷰 관리
POST /api/v1/novels/{novel_id}/reviews
GET  /api/v1/novels/{novel_id}/reviews
PUT  /api/v1/reviews/{review_id}
DELETE /api/v1/reviews/{review_id}

// 리뷰 상호작용
POST /api/v1/reviews/{review_id}/helpful
POST /api/v1/reviews/{review_id}/comments
POST /api/v1/reviews/{review_id}/report

// 사용자 관련
GET  /api/v1/users/{user_id}/reviews
GET  /api/v1/users/{user_id}/ratings
GET  /api/v1/users/{user_id}/trust-score
```

### 6.2 관리자 API
```javascript
// 모더레이션
GET  /api/v1/admin/reports
PUT  /api/v1/admin/reports/{report_id}/resolve
GET  /api/v1/admin/reviews/flagged
PUT  /api/v1/admin/reviews/{review_id}/moderate

// 통계 및 분석
GET  /api/v1/admin/analytics/reviews
GET  /api/v1/admin/analytics/ratings
GET  /api/v1/admin/analytics/users/trust-scores
```

### 6.3 외부 시스템 연동
- **추천 시스템**: 평점/리뷰 데이터 실시간 스트리밍
- **알림 시스템**: 리뷰 등록, 댓글 알림
- **검색 엔진**: 리뷰 텍스트 색인화
- **분석 플랫폼**: 텍스트 분석 결과 연동

## 7. 제약사항

### 7.1 기술적 제약사항
- **텍스트 분석**: 한국어 자연어 처리 성능 한계
- **실시간 처리**: 대용량 텍스트 분석 지연 가능성
- **저장소**: 리뷰 텍스트 데이터 급속 증가
- **캐싱**: 개인화된 리뷰 목록 캐싱 복잡성

### 7.2 비즈니스 제약사항
- **표현의 자유**: 과도한 검열로 인한 사용자 이탈
- **공정성**: 모든 작품에 공평한 평가 기회 제공
- **작가 보호**: 악의적 리뷰로부터 작가 보호
- **사용자 경험**: 복잡한 신고/검토 프로세스 간소화

### 7.3 법적 제약사항
- **명예훼손**: 작가/작품에 대한 근거 없는 비방 방지
- **저작권**: 리뷰 내 작품 내용 과도한 인용 제한
- **개인정보**: 리뷰 내 개인정보 노출 방지
- **아동 보호**: 성인 콘텐츠 리뷰 연령 제한

### 7.4 운영 제약사항
- **모더레이션**: 24시간 신고 처리 인력 한계
- **다국어**: 초기 한국어만 지원, 향후 확장
- **스팸 대응**: 지속적인 스팸 패턴 업데이트 필요
- **품질 관리**: 리뷰 품질 기준 주관성

## 부록

### A. 평점 척도 정의
```
5점: 최고의 작품, 강력 추천
4점: 좋은 작품, 추천
3점: 보통, 취향에 따라
2점: 아쉬운 작품, 비추천
1점: 읽기 어려운 작품, 강력 비추천
```

### B. 스포일러 탐지 키워드 예시
- **결말 관련**: "결국", "마지막에", "엔딩", "끝에서"
- **사망 관련**: "죽는다", "사망", "희생", "살해"
- **반전 관련**: "정체", "진범", "사실은", "알고보니"
- **관계 관련**: "결혼", "이별", "배신", "편이다"

### C. 리뷰 품질 가이드라인
1. **구체적 평가**: 단순 "재밌다"보다는 구체적 이유 제시
2. **건설적 비판**: 비판도 근거와 함께 건설적으로
3. **스포일러 주의**: 핵심 내용 공개 시 반드시 스포일러 태그
4. **존중**: 작가와 다른 독자에 대한 기본적 존중
5. **관련성**: 해당 작품과 관련된 내용만 포함
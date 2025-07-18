# 웹소설나침반 - 사용자 관리 시스템 요구사항 명세서

## 문서 정보

- **프로젝트명**: 웹소설나침반 (WebNovel Compass)
- **문서 버전**: 2.0
- **작성일**: 2025-07-04
- **최종 수정일**: 2025-07-14
- **문서 유형**: 사용자 관리 시스템 요구사항 명세서

## 목차

1. [개요](#1-개요)
2. [기능 요구사항](#2-기능-요구사항)
3. [비기능 요구사항](#3-비기능-요구사항)
4. [데이터 요구사항](#4-데이터-요구사항)
5. [보안 요구사항](#5-보안-요구사항)
6. [인터페이스 요구사항](#6-인터페이스-요구사항)
7. [제약사항](#7-제약사항)

## 1. 개요

### 1.1 목적

웹소설 추천 시스템에서 사용자 정보를 안전하고 효율적으로 관리하기 위한 사용자 관리 시스템의 요구사항을 정의한다.

### 1.2 범위

- 사용자 회원가입, 로그인, 프로필 관리
- 사용자 취향 및 선호도 관리 (점수 기반 정교한 선호도 시스템)
- 인증 및 보안 관리
- 개인정보 보호 및 동의 관리
- 소셜 로그인 연동

### 1.3 용어 정의

- **사용자**: 웹소설 추천 서비스를 이용하는 개인
- **프로필**: 사용자의 기본 정보 및 설정
- **선호도**: 사용자의 웹소설 장르/태그/작가에 대한 점수 기반 선호도 (-1.0 ~ 1.0)
- **명시적 선호도**: 사용자가 직접 설정한 선호도
- **암묵적 선호도**: 사용자 행동 데이터를 기반으로 시스템이 학습한 선호도
- **세션**: 사용자 로그인 상태 유지 정보

## 2. 기능 요구사항

### 2.1 사용자 계정 관리

#### 2.1.1 회원가입 (REQ-USER-001)

**기능 설명**: 신규 사용자의 계정 생성
**입력**: 이메일, 비밀번호, 닉네임, 개인정보 처리 동의
**처리**:

- 이메일 중복 검증
- 닉네임 중복 검증
- 비밀번호 정책 검증
- 이메일 인증 발송
- 기본 선호도 설정 생성 (중립값으로 초기화)

**출력**: 계정 생성 성공/실패, 이메일 인증 안내
**예외처리**: 중복 계정, 잘못된 이메일 형식, 비밀번호 정책 위반

#### 2.1.2 로그인 (REQ-USER-002)

**기능 설명**: 기존 사용자의 인증 및 세션 생성
**입력**: 이메일, 비밀번호
**처리**:

- 계정 존재 여부 확인
- 비밀번호 검증
- 계정 상태 확인 (활성/휴면/정지)
- JWT 토큰 생성
- 로그인 통계 업데이트 (등급 계산용)

**출력**: 로그인 성공/실패, 액세스 토큰, 리프레시 토큰
**예외처리**: 잘못된 인증 정보, 계정 잠금, 정지된 계정

#### 2.1.3 로그아웃 (REQ-USER-003)

**기능 설명**: 사용자 세션 종료
**입력**: 액세스 토큰
**처리**: 토큰 무효화, 세션 삭제
**출력**: 로그아웃 성공 확인

#### 2.1.4 비밀번호 재설정 (REQ-USER-004)

**기능 설명**: 비밀번호 분실 시 재설정
**입력**: 이메일 주소
**처리**:

- 계정 존재 확인
- 재설정 토큰 생성 (30분 유효)
- 이메일 발송

**출력**: 재설정 링크 발송 완료

### 2.2 프로필 관리

#### 2.2.1 프로필 조회 (REQ-USER-005)

**기능 설명**: 사용자 프로필 정보 조회
**입력**: 사용자 ID
**출력**: 프로필 정보 (닉네임, 가입일, 등급, 프로필 이미지, 선호도 요약 등)

#### 2.2.2 프로필 수정 (REQ-USER-006)

**기능 설명**: 사용자 프로필 정보 수정
**입력**: 수정할 프로필 정보
**처리**:

- 닉네임 중복 확인
- 프로필 이미지 업로드 및 검증

**출력**: 수정 성공/실패
**예외처리**: 닉네임 중복, 이미지 용량 초과

#### 2.2.3 계정 탈퇴 (REQ-USER-007)

**기능 설명**: 사용자 계정 삭제
**입력**: 사용자 ID, 탈퇴 사유
**처리**:

- 비밀번호 재확인
- 관련 데이터 익명화/삭제 처리 (선호도 데이터 포함)
- 30일 복구 기간 설정

**출력**: 탈퇴 처리 완료

### 2.3 사용자 선호도 관리

#### 2.3.1 명시적 선호도 설정 (REQ-USER-008)

**기능 설명**: 사용자가 직접 설정하는 선호도 관리
**입력**:

- 장르별 선호도 점수 (-1.0 ~ 1.0)
- 태그별 선호도 점수 (-1.0 ~ 1.0)
- 작가별 선호도 점수 (-1.0 ~ 1.0)
- 기본 설정 (성인 콘텐츠 필터, 선호 길이, 연재 상태 등)

**처리**:

- 점수 범위 검증 (-1.0 ~ 1.0)
- 명시적 선호도로 플래그 설정
- 신뢰도 100%로 설정
- 추천 시스템에 즉시 반영

**출력**: 설정 완료 확인, 적용된 선호도 요약
**예외처리**: 잘못된 점수 범위, 존재하지 않는 장르/태그/작가

#### 2.3.2 암묵적 선호도 학습 (REQ-USER-009)

**기능 설명**: 사용자 행동 데이터 기반 자동 선호도 분석 및 업데이트
**입력**: 사용자 행동 데이터 (평점, 클릭, 조회 시간, 북마크 등)
**처리**:

- 행동 데이터를 선호도 점수로 변환
- 기존 암묵적 선호도와 가중 평균 계산
- 신뢰도 점진적 증가 (최대 0.8)
- 명시적 선호도보다 낮은 우선순위 적용

**알고리즘**:

```
새로운_선호도 = (기존_선호도 * 기존_신뢰도 + 행동_기반_점수 * 행동_가중치) / (기존_신뢰도 + 행동_가중치)
신뢰도 = min(기존_신뢰도 + 0.1, 0.8)  // 명시적 설정(1.0)보다 낮게 유지
```

**출력**: 업데이트된 선호도 정보
**비동기 처리**: 실시간 추천에 영향을 주지 않도록 배치 처리

#### 2.3.3 선호도 조회 및 분석 (REQ-USER-010)

**기능 설명**: 사용자 선호도 현황 조회 및 분석 정보 제공
**입력**: 사용자 ID
**출력**:

- 장르별 선호도 순위 (상위 10개)
- 태그별 선호도 순위 (상위 20개)
- 선호 작가 목록 (상위 10명)
- 선호도 변화 트렌드 (최근 30일)
- 명시적/암묵적 선호도 비율

**시각화**: 선호도 레이더 차트, 트렌드 그래프

#### 2.3.4 선호도 초기화 및 재설정 (REQ-USER-011)

**기능 설명**: 선호도 데이터 초기화 및 재설정
**입력**: 초기화 범위 (전체/장르별/태그별/작가별)
**처리**:

- 선택된 범위의 선호도 데이터 삭제 또는 중립값(0.0) 설정
- 신뢰도 초기값(0.5)으로 재설정
- 추천 시스템 캐시 무효화

**출력**: 초기화 완료 확인
**제한사항**: 사용자당 월 1회만 전체 초기화 가능

### 2.4 소셜 로그인

#### 2.4.1 소셜 계정 연동 (REQ-USER-012)

**기능 설명**: 외부 소셜 계정과 연동
**입력**: 소셜 플랫폼 인증 정보 (Google, Naver, Kakao)
**처리**: OAuth 2.0 인증 처리, 계정 연결
**출력**: 연동 성공/실패

#### 2.4.2 소셜 로그인 (REQ-USER-013)

**기능 설명**: 소셜 계정을 통한 로그인
**입력**: 소셜 플랫폼 인증 토큰
**처리**: 소셜 계정 확인, 기존 계정 매칭, JWT 토큰 생성
**출력**: 로그인 성공, 액세스 토큰

### 2.5 사용자 등급 시스템

#### 2.5.1 등급 계산 (REQ-USER-014)

**기능 설명**: 사용자 활동 기반 등급 산정
**입력**: 사용자 활동 데이터
**처리**:

- 활동 점수 계산 (로그인, 리뷰 작성, 평점 참여, 선호도 설정)
- 등급 업데이트 (브론즈, 실버, 골드, 플래티넘, 다이아몬드)

**점수 계산**:

- 일일 로그인: 10점
- 평점 등록: 20점
- 리뷰 작성: 50점
- 명시적 선호도 설정: 30점
- 유용한 리뷰 작성 (좋아요 받은 경우): 추가 10-50점

**출력**: 현재 등급, 다음 등급까지 필요 점수

### 2.6 알림 및 설정 관리

#### 2.6.1 알림 설정 (REQ-USER-015)

**기능 설명**: 사용자 알림 설정 관리
**입력**: 알림 유형별 수신 설정 (이메일, 푸시, SMS)
**알림 유형**:

- 새로운 추천 작품 알림
- 선호 작가 신작 알림
- 리뷰/평점에 대한 반응 알림
- 시스템 공지사항

**출력**: 설정 저장 완료

#### 2.6.2 개인화 설정 (REQ-USER-016)

**기능 설명**: 추천 알고리즘 개인화 설정
**입력**:

- 추천 알고리즘 가중치 설정 (협업 필터링 vs 콘텐츠 기반)
- 추천 민감도 (보수적/균형/모험적)
- 다양성 선호도 (유사한 작품 vs 다양한 작품)

**처리**: 추천 시스템에 설정값 반영
**출력**: 설정 적용 완료

## 3. 비기능 요구사항

### 3.1 성능 요구사항

- **응답 시간**: 모든 API 200ms 이하
- **선호도 조회**: 100ms 이하 (캐싱 활용)
- **선호도 업데이트**: 50ms 이하 (실시간 반영)
- **동시 사용자**: 1,000명 이상 지원
- **가용성**: 99.9% 이상
- **처리량**: 초당 100건 이상의 로그인 처리

### 3.2 확장성 요구사항

- **사용자 확장**: 100만 명까지 확장 가능한 구조
- **선호도 데이터**: 사용자당 1,000개 이상의 선호도 항목 지원
- **지역 확장**: 다국가 서비스 대응 가능
- **마이크로서비스**: 독립적인 서비스 배포 및 확장

### 3.3 사용성 요구사항

- **직관적 UI**: 3단계 이내 모든 기능 접근
- **선호도 설정**: 직관적인 슬라이더/별점 인터페이스
- **다국어 지원**: 한국어, 영어 지원
- **접근성**: WCAG 2.1 AA 수준 준수
- **반응형**: 모바일, 태블릿, 데스크톱 지원

## 4. 데이터 요구사항

### 4.1 사용자 기본 정보

```sql
users (
    user_id BIGINT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nickname VARCHAR(50) UNIQUE NOT NULL,
    status ENUM('ACTIVE', 'DORMANT', 'SUSPENDED', 'DELETED') DEFAULT 'ACTIVE',

    -- 선택 데이터
    birth_date DATE,
    gender ENUM('MALE', 'FEMALE', 'OTHER', 'PREFER_NOT_TO_SAY'),
    phone_number VARCHAR(20),
    profile_image_url VARCHAR(500),
    bio VARCHAR(100),

    -- 활동 데이터
    last_login_at TIMESTAMP,
    login_count INT DEFAULT 0,
    activity_score INT DEFAULT 0,
    user_level ENUM('BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND') DEFAULT 'BRONZE',

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    INDEX idx_email (email),
    INDEX idx_nickname (nickname),
    INDEX idx_status_created (status, created_at),
    INDEX idx_last_login (last_login_at)
)
```

### 4.2 사용자 기본 설정 정보

```sql
user_preferences (
    user_id BIGINT PRIMARY KEY,

    -- 콘텐츠 필터링 설정
    adult_content_filter BOOLEAN DEFAULT FALSE,
    preferred_length ENUM('SHORT', 'MEDIUM', 'LONG', 'ANY') DEFAULT 'ANY',
    preferred_status ENUM('COMPLETED', 'ONGOING', 'ANY') DEFAULT 'ANY',

    -- 추천 알고리즘 설정
    recommendation_sensitivity ENUM('CONSERVATIVE', 'BALANCED', 'ADVENTUROUS') DEFAULT 'BALANCED',
    algorithm_weight_collaborative DECIMAL(3,2) DEFAULT 0.60, -- 협업 필터링 가중치
    algorithm_weight_content_based DECIMAL(3,2) DEFAULT 0.40, -- 콘텐츠 기반 가중치
    diversity_preference DECIMAL(3,2) DEFAULT 0.5, -- 다양성 선호도 (0.0: 유사작품, 1.0: 다양한작품)

    -- 알림 설정
    notification_email BOOLEAN DEFAULT TRUE,
    notification_push BOOLEAN DEFAULT TRUE,
    notification_new_recommendations BOOLEAN DEFAULT TRUE,
    notification_author_updates BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
)
```

### 4.3 장르 선호도 테이블

```sql
user_genre_preferences (
    preference_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    genre_id INT NOT NULL,

    -- 핵심: 점수 기반 선호도
    preference_score DECIMAL(3,2) NOT NULL, -- -1.0(매우 싫어함) ~ 1.0(매우 좋아함)

    -- 선호도 메타데이터
    is_explicit BOOLEAN DEFAULT FALSE, -- true: 사용자 직접 설정, false: 시스템 학습
    confidence_level DECIMAL(3,2) DEFAULT 0.5, -- 신뢰도 (0.0 ~ 1.0)

    -- 학습 정보
    interaction_count INT DEFAULT 1, -- 해당 장르 상호작용 횟수
    last_interaction_type VARCHAR(50), -- 'RATING', 'VIEW', 'BOOKMARK', 'SEARCH', etc.
    last_updated_by VARCHAR(20) DEFAULT 'SYSTEM', -- 'USER' or 'SYSTEM'

    -- 시간 정보
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    UNIQUE KEY unique_user_genre (user_id, genre_id),
    INDEX idx_user_score (user_id, preference_score DESC),
    INDEX idx_confidence (confidence_level DESC),
    INDEX idx_explicit (is_explicit, preference_score DESC),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
)
```

### 4.4 태그 선호도 테이블

```sql
user_tag_preferences (
    preference_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    tag_id INT NOT NULL,
    preference_score DECIMAL(3,2) NOT NULL, -- -1.0 ~ 1.0
    is_explicit BOOLEAN DEFAULT FALSE,
    confidence_level DECIMAL(3,2) DEFAULT 0.5,
    interaction_count INT DEFAULT 1,
    last_interaction_type VARCHAR(50),
    last_updated_by VARCHAR(20) DEFAULT 'SYSTEM',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    UNIQUE KEY unique_user_tag (user_id, tag_id),
    INDEX idx_user_score (user_id, preference_score DESC),
    INDEX idx_confidence (confidence_level DESC),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
)
```

### 4.5 작가 선호도 테이블

```sql
user_author_preferences (
    preference_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    author_id BIGINT NOT NULL,
    preference_score DECIMAL(3,2) NOT NULL, -- -1.0 ~ 1.0
    is_explicit BOOLEAN DEFAULT FALSE,
    confidence_level DECIMAL(3,2) DEFAULT 0.5,

    -- 작가별 특화 정보
    read_count INT DEFAULT 0, -- 해당 작가 작품 읽은 수
    avg_rating DECIMAL(3,2), -- 해당 작가 작품들에 준 평균 평점
    follow_status BOOLEAN DEFAULT FALSE, -- 작가 팔로우 여부

    interaction_count INT DEFAULT 1,
    last_interaction_type VARCHAR(50),
    last_updated_by VARCHAR(20) DEFAULT 'SYSTEM',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    UNIQUE KEY unique_user_author (user_id, author_id),
    INDEX idx_user_score (user_id, preference_score DESC),
    INDEX idx_follow (follow_status, preference_score DESC),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES authors(author_id)
)
```

### 4.6 선호도 변경 이력 테이블

```sql
user_preference_history (
    history_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    preference_type ENUM('GENRE', 'TAG', 'AUTHOR') NOT NULL,
    target_id BIGINT NOT NULL, -- genre_id, tag_id, author_id

    -- 변경 내용
    old_score DECIMAL(3,2),
    new_score DECIMAL(3,2),
    change_reason VARCHAR(100), -- 'USER_SETTING', 'BEHAVIOR_LEARNING', 'RATING_UPDATE', etc.
    changed_by VARCHAR(20), -- 'USER' or 'SYSTEM'

    created_at TIMESTAMP DEFAULT NOW(),

    INDEX idx_user_created (user_id, created_at),
    INDEX idx_preference_type (preference_type, created_at),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
)
```

### 4.7 동의 관리 정보

```sql
user_consents (
    consent_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,

    -- 법적 동의
    terms_of_service BOOLEAN DEFAULT FALSE,
    privacy_policy BOOLEAN DEFAULT FALSE,

    -- 마케팅 동의
    marketing_email BOOLEAN DEFAULT FALSE,
    marketing_sms BOOLEAN DEFAULT FALSE,
    marketing_push BOOLEAN DEFAULT FALSE,

    -- 개인화 동의
    personalization BOOLEAN DEFAULT TRUE, -- 추천 서비스 이용
    behavior_tracking BOOLEAN DEFAULT TRUE, -- 행동 데이터 수집
    cookies BOOLEAN DEFAULT TRUE,

    consented_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
)
```

### 4.8 소셜 계정 연동

```sql
user_social_accounts (
    social_account_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    provider ENUM('GOOGLE', 'NAVER', 'KAKAO', 'APPLE') NOT NULL,
    provider_id VARCHAR(255) NOT NULL,
    provider_email VARCHAR(255),
    is_primary BOOLEAN DEFAULT FALSE,
    connected_at TIMESTAMP DEFAULT NOW(),
    last_used_at TIMESTAMP,

    UNIQUE KEY unique_provider_id (provider, provider_id),
    INDEX idx_user_provider (user_id, provider),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
)
```

## 5. 보안 요구사항

### 5.1 인증 보안

- **비밀번호 정책**: 최소 8자, 대소문자+숫자+특수문자 조합 필수
- **해싱**: BCrypt 알고리즘 사용, Salt 추가
- **토큰 보안**: JWT 토큰, 액세스 토큰 15분, 리프레시 토큰 7일
- **세션 관리**: 동시 세션 5개 제한

### 5.2 접근 제어

- **권한 기반**: RBAC (Role-Based Access Control) 적용
- **API 제한**: Rate Limiting 적용 (사용자당 분당 60회)
- **IP 제한**: 의심스러운 IP 자동 차단
- **로그인 제한**: 5회 실패 시 30분 계정 잠금

### 5.3 데이터 보호

- **암호화**: 개인정보 AES-256 암호화
- **전송 보안**: HTTPS/TLS 1.3 필수
- **선호도 데이터 보호**: 민감한 취향 정보 암호화 저장
- **데이터 익명화**: 분석용 데이터 개인 식별 불가 처리
- **감사 로그**: 모든 민감한 작업 로깅

### 5.4 개인정보 보호

- **GDPR 준수**: EU 개인정보 보호 규정 준수
- **데이터 최소화**: 필요 최소한의 정보만 수집
- **삭제 권리**: 사용자 요청 시 30일 내 완전 삭제 (선호도 데이터 포함)
- **투명성**: 개인정보 처리 현황 대시보드 제공
- **선호도 데이터 이용 동의**: 개인화 서비스 이용 동의 별도 관리

## 6. 인터페이스 요구사항

### 6.1 사용자 인터페이스

- **웹 브라우저**: Chrome, Firefox, Safari, Edge 최신 2개 버전
- **모바일**: iOS 13+, Android 8+ 지원
- **반응형**: 320px ~ 1920px 해상도 대응
- **접근성**: 키보드 네비게이션, 스크린 리더 지원
- **선호도 설정 UI**: 직관적인 슬라이더, 별점, 태그 선택 인터페이스

### 6.2 API 인터페이스

```
# 인증 관련
POST /api/v1/auth/register              # 회원가입
POST /api/v1/auth/login                 # 로그인
POST /api/v1/auth/logout                # 로그아웃
POST /api/v1/auth/refresh               # 토큰 갱신
POST /api/v1/auth/social/{provider}     # 소셜 로그인

# 프로필 관리
GET  /api/v1/users/profile              # 프로필 조회
PUT  /api/v1/users/profile              # 프로필 수정
PUT  /api/v1/users/settings             # 기본 설정 변경
DELETE /api/v1/users/account            # 계정 탈퇴

# 선호도 관리
GET  /api/v1/users/preferences          # 전체 선호도 조회
GET  /api/v1/users/preferences/summary  # 선호도 요약 정보
PUT  /api/v1/users/preferences/genres   # 장르 선호도 설정
PUT  /api/v1/users/preferences/tags     # 태그 선호도 설정
PUT  /api/v1/users/preferences/authors  # 작가 선호도 설정
POST /api/v1/users/preferences/reset    # 선호도 초기화
GET  /api/v1/users/preferences/history  # 선호도 변경 이력

# 알림 및 설정
GET  /api/v1/users/notifications        # 알림 설정 조회
PUT  /api/v1/users/notifications        # 알림 설정 변경
GET  /api/v1/users/consents             # 동의 현황 조회
PUT  /api/v1/users/consents             # 동의 설정 변경
```

### 6.3 외부 시스템 연동

- **소셜 로그인**: Google OAuth 2.0, Naver Login, Kakao Login
- **이메일**: SMTP 서버 연동 (SendGrid, AWS SES)
- **SMS**: 문자 발송 서비스 연동
- **파일 저장**: AWS S3, CloudFront CDN
- **추천 시스템**: 선호도 데이터 실시간 동기화
- **행동 추적 시스템**: 사용자 행동 데이터 수신

### 6.4 내부 시스템 연동

```
# 추천 시스템과의 연동
POST /internal/v1/preferences/update    # 선호도 변경 알림
GET  /internal/v1/users/{id}/profile    # 사용자 프로필 조회
POST /internal/v1/users/behavior        # 행동 데이터 기반 선호도 업데이트

# 분석 시스템과의 연동
GET  /internal/v1/users/{id}/preferences # 분석용 선호도 데이터
POST /internal/v1/users/segments        # 사용자 세그먼트 분류
```

## 7. 제약사항

### 7.1 기술적 제약사항

- **데이터베이스**: PostgreSQL 12+ 사용
- **캐시**: Redis 6+ 사용 (선호도 데이터 캐싱)
- **언어**: Java 17+ (Spring Boot), Python 3.9+ (FastAPI)
- **컨테이너**: Docker 기반 배포
- **선호도 정밀도**: DECIMAL(3,2) 범위 (-1.00 ~ 1.00)

### 7.2 운영 제약사항

- **서비스 시간**: 24시간 365일 운영
- **점검 시간**: 월 1회 최대 2시간 점검 (선호도 데이터 백업 포함)
- **백업**: 일일 자동 백업, 30일 보관
- **모니터링**: 실시간 시스템 상태 모니터링
- **선호도 동기화**: 추천 시스템과 5분 이내 동기화 보장

### 7.3 법적 제약사항

- **개인정보보호법**: 국내법 준수 (선호도 데이터 포함)
- **GDPR**: EU 서비스 확장 시 준수
- **전자상거래법**: 사용자 정보 5년 보관
- **청소년보호법**: 19세 미만 성인 콘텐츠 차단
- **선호도 데이터 보호**: 개인 취향 정보 특별 보호

### 7.4 비즈니스 제약사항

- **무료 서비스**: 기본 기능 무료 제공
- **프리미엄**: 고급 선호도 분석 기능 유료 서비스
- **광고**: 개인정보 기반 타겟팅 광고 금지
- **데이터 판매**: 사용자 개인정보 외부 판매 금지
- **선호도 데이터 활용**: 추천 서비스 목적으로만 제한 사용

### 7.5 성능 제약사항

- **선호도 업데이트**: 사용자당 일일 1,000회 이하
- **대량 설정 변경**: 동시에 50개 이상 선호도 변경 시 순차 처리
- **캐시 TTL**: 선호도 캐시 최대 1시간 유지
- **배치 처리**: 암묵적 선호도 학습은 야간 배치로 처리

## 부록

### A. 선호도 점수 가이드라인

```
점수 범위 및 의미:
 1.0: 매우 좋아함 (적극 추천 희망)
 0.7: 좋아함 (추천 희망)
 0.3: 약간 좋아함 (가끔 추천)
 0.0: 중립 (상관없음)
-0.3: 약간 싫어함 (피하고 싶음)
-0.7: 싫어함 (추천하지 않음)
-1.0: 매우 싫어함 (절대 추천하지 않음)
```

### B. 신뢰도 계산 방식

```
명시적 선호도: 1.0 (100% 신뢰)
암묵적 선호도: 0.1 ~ 0.8 (상호작용 횟수와 일관성에 따라)

신뢰도 업데이트 공식:
새_신뢰도 = min(기존_신뢰도 + (상호작용_일관성 * 0.1), 0.8)
```

### C. 선호도 학습 알고리즘

```python
# 행동 데이터를 선호도 점수로 변환
def behavior_to_preference_score(interaction_type, value, duration):
    if interaction_type == 'RATING':
        return (value - 3.0) / 2.0  # 1-5점을 -1.0~1.0으로 변환
    elif interaction_type == 'VIEW':
        return min(duration / 300.0, 0.5)  # 5분 이상 조회 시 0.5점
    elif interaction_type == 'BOOKMARK':
        return 0.8  # 북마크는 강한 선호 의미
    elif interaction_type == 'SEARCH':
        return 0.3  # 검색은 관심 표현
    else:
        return 0.1  # 기타 상호작용
```

### D. 선호도 데이터 마이그레이션 가이드

```sql
-- 기존 이분법 데이터를 점수 기반으로 변환
UPDATE user_genre_preferences
SET preference_score = CASE
    WHEN old_preference = 'LIKE' THEN 0.7
    WHEN old_preference = 'DISLIKE' THEN -0.7
    ELSE 0.0
END,
confidence_level = CASE
    WHEN old_preference IN ('LIKE', 'DISLIKE') THEN 1.0
    ELSE 0.5
END,
is_explicit = CASE
    WHEN old_preference IN ('LIKE', 'DISLIKE') THEN TRUE
    ELSE FALSE
END;
```

### E. 용어집

- **JWT**: JSON Web Token, 웹 표준 토큰
- **OAuth**: 인증을 위한 개방형 표준
- **RBAC**: 역할 기반 접근 제어
- **GDPR**: EU 일반 데이터 보호 규정
- **TLS**: 전송 계층 보안 프로토콜
- **선호도 점수**: 사용자의 특정 항목에 대한 정량화된 선호도 (-1.0 ~ 1.0)
- **신뢰도**: 선호도 데이터의 정확성과 신뢰성을 나타내는 지표 (0.0 ~ 1.0)

### F. 참고 문서

- 웹소설나침반 시스템 아키텍처 문서
- 추천 시스템 요구사항 명세서
- 사용자 행동 추적 시스템 요구사항 명세서
- API 설계 가이드라인
- 데이터베이스 설계 문서
- 보안 정책 문서

---

**주요 변경사항 (07-14)**

- 이분법적 선호도 시스템을 점수 기반 시스템으로 전면 개편
- 명시적/암묵적 선호도 구분 및 신뢰도 관리 추가
- 선호도 변경 이력 추적 기능 추가
- 추천 시스템과의 연동 인터페이스 강화
- 성능 및 확장성 요구사항 구체화

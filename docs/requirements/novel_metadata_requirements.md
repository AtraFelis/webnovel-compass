# 웹소설나침반 - 웹소설 메타데이터 관리 시스템 요구사항 명세서

## 문서 정보

- **프로젝트명**: 웹소설나침반 (WebNovel Compass)
- **문서 버전**: 1.0
- **작성일**: 2025-07-04
- **문서 유형**: 웹소설 메타데이터 관리 시스템 요구사항 명세서

## 목차

1. [개요](#1-개요)
2. [기능 요구사항](#2-기능-요구사항)
   - 2.1 [웹소설 기본 정보 관리](#21-웹소설-기본-정보-관리)
   - 2.2 [작가 정보 관리](#22-작가-정보-관리)
   - 2.3 [장르 및 분류 체계 관리](#23-장르-및-분류-체계-관리)
   - 2.4 [연재 정보 관리](#24-연재-정보-관리)
   - 2.5 [통계 및 인기도 관리](#25-통계-및-인기도-관리)
   - 2.6 [미디어 파일 관리](#26-미디어-파일-관리)
   - 2.7 [검색 및 필터링](#27-검색-및-필터링)
3. [비기능 요구사항](#3-비기능-요구사항)
4. [데이터 요구사항](#4-데이터-요구사항)
5. [보안 요구사항](#5-보안-요구사항)
6. [인터페이스 요구사항](#6-인터페이스-요구사항)
7. [제약사항](#7-제약사항)

## 1. 개요

### 1.1 목적

웹소설 추천 시스템에서 웹소설 작품 정보를 체계적으로 관리하고, 추천 알고리즘에 필요한 메타데이터를 효율적으로 제공하기 위한 시스템의 요구사항을 정의한다.

### 1.2 범위

- 웹소설 기본 정보 관리 (제목, 작가, 장르, 줄거리 등)
- 분류 체계 관리 (장르, 태그, 카테고리)
- 연재 정보 관리 (회차, 업데이트 상태)
- 통계 데이터 관리 (조회수, 평점, 인기도)
- 미디어 파일 관리 (표지, 썸네일)

### 1.3 용어 정의

- **웹소설**: 온라인 플랫폼에서 연재되는 소설 작품
- **메타데이터**: 웹소설을 설명하는 구조화된 정보
- **장르**: 작품의 주요 분류 체계 (로맨스, 판타지, 무협 등)
- **태그**: 작품의 세부 특성을 나타내는 키워드
- **연재 상태**: 작품의 발행 상태 (연재중, 완결, 휴재, 중단)

## 2. 기능 요구사항

### 2.1 웹소설 기본 정보 관리

#### 2.1.1 웹소설 등록 (REQ-NOVEL-001)

**기능 설명**: 새로운 웹소설 작품 정보 등록
**입력**:

- 필수: 제목, 작가명, 줄거리, 주요 장르
- 선택: 작가 소개, 출판사
  **처리**:
- 제목 중복 검사 (동일 작가)
- 작가 정보 연동 또는 신규 생성
- 고유 식별자 생성
- 초기 상태 설정
  **출력**: 웹소설 ID, 등록 성공/실패
  **예외처리**: 제목 중복, 필수 정보 누락, 부적절한 콘텐츠

#### 2.1.2 웹소설 정보 수정 (REQ-NOVEL-002)

**기능 설명**: 기존 웹소설 정보 수정
**입력**: 웹소설 ID, 수정할 정보
**처리**:

- 권한 확인 (작가 본인 또는 관리자)
- 변경 이력 기록
- 연관 데이터 동기화
  **출력**: 수정 성공/실패
  **예외처리**: 권한 없음, 존재하지 않는 작품

#### 2.1.3 웹소설 정보 조회 (REQ-NOVEL-003)

**기능 설명**: 웹소설 상세 정보 조회
**입력**: 웹소설 ID 또는 검색 조건
**출력**: 웹소설 전체 정보, 통계 데이터
**성능 요구사항**: 100ms 이하 응답 시간

#### 2.1.4 웹소설 삭제 (REQ-NOVEL-004)

**기능 설명**: 웹소설 정보 삭제 (논리 삭제)
**입력**: 웹소설 ID, 삭제 사유
**처리**:

- 권한 확인 (관리자만 가능)
- 논리 삭제 처리 (status = 'DELETED')
- 관련 추천 데이터 무효화
  **출력**: 삭제 성공/실패

### 2.2 작가 정보 관리

#### 2.2.1 작가 등록 (REQ-AUTHOR-001)

**기능 설명**: 작가 정보 등록 및 관리
**입력**: 작가명, 프로필 정보, 소개
**처리**:

- 작가명 중복 확인
- 필명 관리 (동일 작가의 여러 필명)
  **출력**: 작가 ID, 등록 성공/실패

#### 2.2.2 작가별 작품 조회 (REQ-AUTHOR-002)

**기능 설명**: 특정 작가의 전체 작품 목록 조회
**입력**: 작가 ID
**출력**: 작품 목록, 작가 통계 정보

### 2.3 장르 및 분류 체계 관리

#### 2.3.1 장르 체계 관리 (REQ-GENRE-001)

**기능 설명**: 웹소설 장르 분류 체계 관리
**요구사항**:

- 주요 장르: 로맨스, 판타지, 무협, 현대판타지, 게임, SF, 추리, 스릴러, 공포, 역사, 에세이
- 계층 구조 지원 (대분류 > 중분류 > 소분류)
- 복수 장르 태깅 가능 (주장르 1개 + 부장르 최대 2개)
  **처리**: 장르별 작품 수 통계 자동 계산

#### 2.3.2 태그 시스템 (REQ-TAG-001)

**기능 설명**: 웹소설 특성을 나타내는 태그 관리
**태그 카테고리**:

- 스토리 특성: 해피엔딩, 배드엔딩, 오픈엔딩, 반전, 떡밥
- 캐릭터 특성: 먼치킨, 약캐, 천재, 열혈, 쿨시크
- 설정 특성: 회귀, 환생, 빙의, 차원이동, 시간여행
- 관계 특성: 삼각관계, 역하렘, 브로맨스, 가족애
- 진행 방식: 단편, 연작, 시리즈, 외전
  **처리**:
- 태그별 인기도 분석
- 사용자 선호 태그 기반 추천

#### 2.3.3 연령 등급 분류 (REQ-RATING-001)

**기능 설명**: 콘텐츠 연령 등급 관리
**등급 체계**:

- 전체 이용가: 모든 연령 적합
- 12세 이상: 가벼운 폭력, 간접적 표현
- 15세 이상: 중간 수준의 폭력, 연애 표현
- 19세 이상: 성인 콘텐츠, 직접적 표현
  **처리**: 미성년자 접근 제한 기능

### 2.4 연재 정보 관리

#### 2.4.1 연재 상태 관리 (REQ-SERIES-001)

**기능 설명**: 웹소설 연재 상태 추적 및 관리
**연재 상태**:

- 연재중 (ONGOING)
- 완결 (COMPLETED)
- 휴재 (HIATUS)
- 중단 (DISCONTINUED)
  **처리**:
- 상태 변경 시 알림 발송
- 연재 일정 관리

#### 2.4.2 회차 정보 관리 (REQ-EPISODE-001)

**기능 설명**: 웹소설 에피소드/회차 정보 관리
**입력**: 회차 번호, 제목, 발행일, 자수, 유료/무료 여부
**처리**:

- 연속된 회차 번호 검증
- 발행 일정 관리
- 유료 회차 결제 연동
  **출력**: 회차 정보, 전체 진행률

#### 2.4.3 연재 통계 (REQ-SERIES-002)

**기능 설명**: 연재 관련 통계 정보 제공
**통계 항목**:

- 총 회차 수, 총 분량(자수)
- 평균 업데이트 주기
- 연재 시작일, 완결일
- 연재 기간, 휴재 기간

### 2.5 통계 및 인기도 관리

#### 2.5.1 조회 통계 (REQ-STATS-001)

**기능 설명**: 웹소설 조회 통계 수집 및 분석
**수집 데이터**:

- 일일/주간/월간 조회수
- 고유 사용자 조회수 (중복 제거)
- 페이지뷰, 체류 시간
- 디바이스별 조회 통계 (모바일/PC)
  **처리**: 실시간 집계 + 배치 처리로 정확도 보장

#### 2.5.2 평점 통계 (REQ-STATS-002)

**기능 설명**: 사용자 평점 통계 관리
**통계 항목**:

- 평균 평점 (소수점 2자리)
- 평점 분포 (1~5점별 개수)
- 평점 참여자 수
- 평점 신뢰도 점수
  **처리**: 신규 평점 등록 시 실시간 업데이트

#### 2.5.3 인기도 지수 (REQ-STATS-003)

**기능 설명**: 종합 인기도 지수 계산
**계산 요소**:

- 조회수 (30%), 평점 (25%), 북마크 수 (20%)
- 리뷰 수 (15%), 최신성 (10%)
  **처리**:
- 주기적 재계산 (매일 새벽 2시)
- 가중치 조정 가능한 구조

### 2.6 미디어 파일 관리

#### 2.6.1 표지 이미지 관리 (REQ-MEDIA-001)

**기능 설명**: 웹소설 표지 이미지 업로드 및 관리
**지원 형식**: JPEG, PNG, WebP
**크기 제한**: 최대 5MB, 권장 비율 3:4
**처리**:

- 자동 리사이징 (썸네일 생성)
- CDN 업로드 및 URL 생성
- 이미지 최적화 (품질 조정)
  **출력**: 원본 URL, 썸네일 URL

#### 2.6.2 미디어 파일 버전 관리 (REQ-MEDIA-002)

**기능 설명**: 표지 변경 이력 관리
**처리**: 이전 버전 보관 (최대 5개)
**기능**: 이전 버전으로 롤백 가능

### 2.7 검색 및 필터링

#### 2.7.1 키워드 검색 (REQ-SEARCH-001)

**기능 설명**: 다양한 검색 조건으로 웹소설 검색
**검색 대상**:

- 웹소설 제목 (주제목, 부제목)
- 작가 필명
- 장르명
- 태그
- 줄거리 키워드
  **처리**:
- Elasticsearch 기반 전문 검색
- 형태소 분석을 통한 한국어 검색 최적화
- 동의어 및 유사어 매칭
- 오타 허용 검색 (편집 거리 2 이내)
- 실시간 검색 인덱스 관리 및 업데이트
  **출력**: 관련도 순 정렬된 웹소설 목록
  **성능**: 검색 응답 시간 200ms 이하

#### 2.7.2 자동완성 기능 (REQ-SEARCH-002)

**기능 설명**: 실시간 검색어 자동완성 제공
**데이터 소스**:

- 인기 웹소설 제목
- 인기 작가명
- 자주 검색되는 키워드
- 트렌딩 태그
  **처리**:
- 타이핑 시 실시간 추천 (최소 2글자)
- 검색 빈도 기반 우선순위
- 개인화 추천 (사용자 검색 이력 반영)
- 검색어 자동완성 인덱스 최적화
  **출력**: 최대 10개 자동완성 후보
  **성능**: 50ms 이하 응답

#### 2.7.3 고급 필터링 (REQ-SEARCH-003)

**기능 설명**: 다중 조건을 조합한 정교한 필터링
**필터 옵션**:

- **장르**: 다중 선택 가능, AND/OR 조건
- **연재 상태**: 연재중, 완결, 휴재, 외전연재중
- **평점 범위**: 1-5점 범위 설정
- **연령 등급**: 전체, 12세, 15세, 19세
- **회차 수**: 단편(~50), 중편(50-200), 장편(200+)
- **업데이트 주기**: 일간, 주간, 월간, 불규칙
- **원본 플랫폼**: 카카오페이지, 네이버시리즈, 문피아 등
  **처리**:
- 실시간 필터 적용
- 필터 조합에 따른 결과 수 미리보기
- 사용자별 필터 설정 저장
  **출력**: 필터링된 웹소설 목록 및 결과 수

#### 2.7.4 정렬 기능 (REQ-SEARCH-004)

**기능 설명**: 검색/필터 결과의 다양한 정렬 옵션
**정렬 기준**:

- **관련도**: 검색어와의 일치도 (기본값)
- **인기도**: 조회수, 북마크 수 가중 점수
- **평점순**: 평균 평점 높은 순
- **최신순**: 최근 업데이트 순
- **완결순**: 완결작 우선 표시
- **개인화**: 사용자 취향 반영 점수
  **처리**:
- 다중 정렬 기준 지원 (1차: 평점, 2차: 인기도)
- 정렬 기준별 캐싱 적용
  **출력**: 선택된 기준으로 정렬된 결과

#### 2.7.5 개인화 검색 (REQ-SEARCH-005)

**기능 설명**: 사용자 취향을 반영한 검색 결과 개인화
**개인화 요소**:

- 사용자 선호 장르 가중치 적용
- 과거 읽은 작품과 유사한 작품 우선 표시
- 평점 패턴 반영 (관대한 평가자 vs 까다로운 평가자)
- 최근 검색 패턴 분석
  **처리**:
- 기본 검색 점수 + 개인화 점수 결합
- 실시간 개인화 적용
- 개인화 강도 사용자 설정 가능 (0-100%)
  **출력**: 개인화된 검색 결과
  **성능**: 개인화 처리로 인한 지연 50ms 이내

#### 2.7.6 검색 결과 관리 (REQ-SEARCH-006)

**기능 설명**: 검색 결과의 효율적인 표시 및 관리
**페이지네이션**:

- 페이지당 20개 결과 표시
- 무한 스크롤 지원
- 다음 페이지 프리로딩
  **결과 표시**:
- 웹소설 기본 정보 (제목, 작가, 평점, 표지)
- 검색어 하이라이팅
- 스니펫 (검색어 주변 텍스트 미리보기)
- 외부 플랫폼 바로가기 링크
  **캐싱**:
- 인기 검색어 결과 캐싱 (30분)
- 사용자별 최근 검색 결과 캐싱 (10분)

## 3. 비기능 요구사항

### 3.1 성능 요구사항

- **조회 성능**: 웹소설 상세 정보 조회 100ms 이하
- **검색 성능**: 키워드 검색 200ms 이하
- **필터링 성능**: 다중 필터 적용 150ms 이하
- **자동완성**: 실시간 자동완성 50ms 이하
- **통계 계산**: 실시간 조회수 집계 10ms 이하
- **이미지 로딩**: CDN을 통한 이미지 로딩 50ms 이하

### 3.2 확장성 요구사항

- **작품 수**: 100만 편 이상 지원
- **동시 조회**: 초당 1,000건 이상 처리
- **저장 용량**: 이미지 파일 10TB 이상 지원
- **검색 인덱스**: 실시간 업데이트 지원

### 3.3 가용성 요구사항

- **시스템 가용성**: 99.9% 이상
- **데이터 백업**: 일일 자동 백업
- **장애 복구**: 30분 이내 서비스 복구
- **CDN 이중화**: 이미지 서비스 중단 방지

## 4. 데이터 요구사항

### 4.1 웹소설 기본 테이블

```sql
-- 웹소설 기본 정보 테이블 (개선버전)
novels (
    novel_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    author_id BIGINT NOT NULL,
    description TEXT,
    publisher VARCHAR(100),
    age_rating ENUM('ALL', 'TEEN', 'MATURE', 'ADULT') DEFAULT 'ALL',


    -- 연재 상태 추가
    status ENUM('PREPARING', 'ONGOING', 'COMPLETED', 'HIATUS', 'DISCONTINUED') DEFAULT 'PREPARING',
    total_episodes INT DEFAULT 0,

    -- 표지
    cover_image_url VARCHAR(500),

    -- 시간 정보
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    published_at TIMESTAMP, -- 연재 시작일
    completed_at TIMESTAMP, -- 완결일
    is_deleted BOOLEAN DEFAULT FALSE,

    -- 외래키
    FOREIGN KEY (author_id) REFERENCES authors(author_id),

    -- 인덱스
    INDEX idx_title (title),
    INDEX idx_author (author_id),
    INDEX idx_status (status),
    INDEX idx_platform (original_platform),
    INDEX idx_published (published_at),
    INDEX idx_status_published (status, published_at),
    INDEX idx_author_status (author_id, status),

    -- 전문 검색
    FULLTEXT INDEX ft_search (title, description)
)
```

### 4.2 작가 정보 테이블

```sql
authors (
    author_id BIGINT PRIMARY KEY,
    pen_names VARCHAR(50),
    profile_text TEXT,
    debut_year YEAR,
    website_url VARCHAR(500),
    social_links JSON,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)
```

### 4.3 장르 및 태그 테이블

```sql
genres (
    genre_id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    parent_id INT,
    display_order INT,
    is_active BOOLEAN DEFAULT TRUE
),

tags (
    tag_id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    category VARCHAR(20), -- 'STORY', 'CHARACTER', 'SETTING', 'RELATIONSHIP'
    usage_count INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE
),

novel_genres (
    id BINGINT PRIMARY KEY,
    id BINGINT PRIMARY KEY,
    novel_id BIGINT,
    genre_id INT,
    is_primary BOOLEAN DEFAULT FALSE,

    FOREIGN KEY (novel_id) REFERENCES novels(novel_id)
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
),

novel_tags (
    id BINGINT PRIMARY KEY,
    novel_id BIGINT,
    tag_id INT,
    weight DECIMAL(3,2) DEFAULT 1.0,

    FOREIGN KEY (novel_id) REFERENCES novels(novel_id)
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
)
```

### 4.4 연재 정보 테이블

```sql
-- 웹소설 기본 정보 테이블
novels (
   novel_id BIGINT PRIMARY KEY AUTO_INCREMENT,
   title VARCHAR(200) NOT NULL,
   author_id BIGINT NOT NULL,
   description TEXT,
   publisher VARCHAR(100),
   age_rating ENUM('ALL', 'TEEN', 'MATURE', 'ADULT') DEFAULT 'ALL',

   -- 연재 상태
   status ENUM('ONGOING', 'COMPLETED', 'HIATUS', 'DISCONTINUED') DEFAULT 'PREPARING',
   total_episodes INT DEFAULT 0,

   -- 이미지
   cover_image_url VARCHAR(500),

   -- 시간 정보
   created_at TIMESTAMP DEFAULT NOW(),
   updated_at TIMESTAMP DEFAULT NOW(),
   published_at TIMESTAMP, -- 연재 시작일
   completed_at TIMESTAMP, -- 완결일
   is_deleted BOOLEAN DEFAULT FALSE,

   -- 외래키
   FOREIGN KEY (author_id) REFERENCES authors(author_id),

   -- 인덱스
   INDEX idx_title (title),
   INDEX idx_author (author_id),
   INDEX idx_status (status),
   INDEX idx_published (published_at),
   INDEX idx_status_published (status, published_at),
   INDEX idx_author_status (author_id, status),

   -- 전문 검색
   FULLTEXT INDEX ft_search (title, description)
)
```

```sql
-- 플랫폼 정보 테이블
platforms (
   platform_id BIGINT PRIMARY KEY AUTO_INCREMENT,
   platform_name VARCHAR(100) NOT NULL, -- 카카오페이지, 네이버시리즈, 문피아 등
   platform_code VARCHAR(20) UNIQUE NOT NULL, -- KAKAO, NAVER, MUNPIA 등
   base_url VARCHAR(200), -- 플랫폼 기본 URL
   created_at TIMESTAMP DEFAULT NOW(),

   INDEX idx_platform_name (platform_name),
   INDEX idx_platform_code (platform_code),
   INDEX idx_active (is_active)
)
```

```sql
-- 웹소설-플랫폼 연결 테이블 (다대다)
novel_platforms (
   novel_id BIGINT NOT NULL,
   platform_id BIGINT NOT NULL,
   platform_novel_id VARCHAR(100) NOT NULL, -- 플랫폼별 작품 ID
   read_url  VARCHAR(500) NOT NULL, -- 해당 플랫폼에서의 작품 URL
   is_original BOOLEAN DEFAULT FALSE, -- 최초 연재 플랫폼 여부
   created_at TIMESTAMP DEFAULT NOW(),

   PRIMARY KEY (novel_id, platform_id),
   UNIQUE KEY unique_platform_novel_id (platform_id, platform_novel_id),

   FOREIGN KEY (novel_id) REFERENCES novels(novel_id) ON DELETE CASCADE,
   FOREIGN KEY (platform_id) REFERENCES platforms(platform_id),

   INDEX idx_novel_platforms_novel (novel_id),
   INDEX idx_novel_platforms_platform (platform_id)
)
```

### 4.5 통계 테이블

```sql
novel_statistics (
    novel_id BIGINT PRIMARY KEY,
    total_views BIGINT DEFAULT 0,
    unique_views BIGINT DEFAULT 0,
    daily_views INT DEFAULT 0,
    weekly_views INT DEFAULT 0,
    monthly_views INT DEFAULT 0,
    average_rating DECIMAL(3,2) DEFAULT 0.0,
    rating_count INT DEFAULT 0,
    bookmark_count INT DEFAULT 0,
    review_count INT DEFAULT 0,
    popularity_score DECIMAL(8,2) DEFAULT 0.0,
    last_updated TIMESTAMP
)
```

### 4.6 미디어 파일 테이블

```sql
novel_images (
    image_id BIGINT PRIMARY KEY,
    novel_id BIGINT NOT NULL,
    image_type ENUM('COVER', 'THUMBNAIL', 'BANNER'),
    original_url VARCHAR(500),
    thumbnail_url VARCHAR(500),
    file_size INT,
    mime_type VARCHAR(50),
    width INT,
    height INT,
    version INT DEFAULT 1,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP
)
```

### 4.7 검색 인덱스 테이블

```sql
search_indexes (
    index_id BIGINT PRIMARY KEY,
    novel_id BIGINT NOT NULL,
    indexed_content TEXT, -- 검색용 전문 텍스트 (제목+작가+줄거리+태그)
    search_keywords JSON, -- 추출된 검색 키워드
    popularity_score DECIMAL(8,2), -- 인기도 점수 (검색 순위용)
    boost_factors JSON, -- 검색 부스팅 요소들
    indexed_at TIMESTAMP DEFAULT NOW(),

    FULLTEXT INDEX ft_content (indexed_content),
    INDEX idx_novel_id (novel_id),
    INDEX idx_popularity (popularity_score DESC),
    FOREIGN KEY (novel_id) REFERENCES novels(novel_id)
),

search_logs (
    log_id BIGINT PRIMARY KEY,
    user_id BIGINT,
    search_query VARCHAR(500) NOT NULL,
    search_filters JSON, -- 적용된 필터들
    result_count INT,
    clicked_novel_ids JSON, -- 클릭된 결과들
    search_time_ms INT, -- 검색 소요 시간
    created_at TIMESTAMP DEFAULT NOW(),

    INDEX idx_user_created (user_id, created_at),
    INDEX idx_query (search_query(100)),
    INDEX idx_created_at (created_at)
)
```

### 5.1 데이터 접근 제어

- **작가 권한**: 자신의 작품만 수정 가능
- **관리자 권한**: 모든 데이터 접근 및 수정
- **일반 사용자**: 공개된 정보만 조회 가능

### 5.2 콘텐츠 보안

- **성인 콘텐츠**: 연령 인증 후 접근
- **저작권 보호**: 무단 복사 방지 기능
- **부적절한 콘텐츠**: 신고 및 검토 시스템

### 5.3 API 보안

- **인증**: JWT 토큰 기반 API 인증
- **권한 검증**: 모든 CUD 작업 시 권한 확인
- **Rate Limiting**: API 호출 제한 (분당 100회)

## 6. 인터페이스 요구사항

### 6.1 API 엔드포인트

```
# 웹소설 관리 (관리자용)
GET    /api/v1/admin/novels        # 웹소설 목록 관리
POST   /api/v1/admin/novels        # 웹소설 정보 등록 (크롤링/제휴)
PUT    /api/v1/admin/novels/{id}   # 웹소설 정보 수정
DELETE /api/v1/admin/novels/{id}   # 웹소설 정보 삭제

# 웹소설 조회 (일반 사용자용)
GET    /api/v1/novels              # 웹소설 목록 조회
GET    /api/v1/novels/{id}         # 웹소설 상세 조회 (외부 링크 포함)

# 작가 관리
GET    /api/v1/authors             # 작가 목록 조회
GET    /api/v1/authors/{id}        # 작가 상세 조회
GET    /api/v1/authors/{id}/novels # 작가별 작품 조회

# 분류 체계
GET    /api/v1/genres              # 장르 목록 조회
GET    /api/v1/tags                # 태그 목록 조회

# 통계 정보
GET    /api/v1/novels/{id}/stats   # 웹소설 통계 조회
GET    /api/v1/stats/popular       # 인기 작품 조회
GET    /api/v1/stats/trending      # 트렌딩 작품 조회

# 미디어 파일
POST   /api/v1/novels/{id}/images  # 이미지 업로드
DELETE /api/v1/images/{id}         # 이미지 삭제

# 검색 및 필터링
GET    /api/v1/search/novels          # 웹소설 통합 검색
GET    /api/v1/search/autocomplete    # 검색어 자동완성
GET    /api/v1/search/suggestions     # 연관 검색어 추천
POST   /api/v1/search/filters         # 고급 필터 적용
GET    /api/v1/search/popular-keywords # 인기 검색어

# 필터링 전용
GET    /api/v1/novels/filter          # 조건별 필터링
GET    /api/v1/novels/genres/{genre_id} # 장르별 웹소설
GET    /api/v1/novels/authors/{author_id} # 작가별 웹소설
```

- **CDN 서비스**: 이미지 파일 저장 및 배포
- **검색 엔진**: Elasticsearch 또는 Solr 연동
- **이미지 처리**: 썸네일 생성 및 최적화 서비스
- **추천 시스템**: Python FastAPI 추천 서비스 연동

## 7. 제약사항

### 7.1 기술적 제약사항

- **데이터베이스**: PostgreSQL 12+ 사용
- **검색 엔진**: Elasticsearch 7+ 사용 (한국어 Nori 분석기 필수)
- **이미지 저장**: AWS S3 또는 호환 스토리지
- **캐싱**: Redis 6+ 사용

### 7.2 비즈니스 제약사항

- **저작권**: 작가 동의 없는 작품 등록 금지
- **성인 콘텐츠**: 법적 규제 준수
- **데이터 보관**: 삭제된 작품 정보 30일 보관
- **상업적 이용**: 작가 수익 배분 정책 준수

### 7.3 운영 제약사항

- **서비스 시간**: 24시간 365일 운영
- **점검 시간**: 월 1회 최대 1시간 점검
- **백업 정책**: 일일 전체 백업, 시간별 증분 백업
- **모니터링**: 실시간 시스템 상태 모니터링

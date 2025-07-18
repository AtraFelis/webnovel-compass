# 웹소설나침반 - 마이크로서비스별 요구사항 분류

## 🏗️ 마이크로서비스 구조

```
User Service (사용자 관리)
Content Service (콘텐츠 관리)
Analytics Service (행동 분석 + 추천 관리)
Recommendation Service (Python FastAPI - AI 추천)
```

---

## 1️⃣ User Service (사용자 관리)

### 📋 담당 요구사항
- **user_management_requirements.md** (전체)

### 🎯 주요 기능
- 사용자 인증/인가 (JWT)
- 회원가입, 로그인, 프로필 관리
- **사용자 선호도 관리** (점수 기반)
- 소셜 로그인 연동
- 사용자 등급 시스템
- 알림 및 설정 관리

### 📊 관리 테이블
```sql
-- 사용자 기본 정보
users
user_preferences (기본 설정)
user_consents (동의 관리)
user_social_accounts (소셜 연동)

-- 선호도 관리 (핵심!)
user_genre_preferences
user_tag_preferences  
user_author_preferences
user_preference_history
```

### 🔗 외부 연동
- 소셜 로그인 (Google, Naver, Kakao)
- 이메일/SMS 서비스
- 추천 시스템 (선호도 데이터 제공)

---

## 2️⃣ Content Service (콘텐츠 관리)

### 📋 담당 요구사항
- **novel_metadata_requirements.md** (전체)
- **rating_review_system_requirements.md** (전체)

### 🎯 주요 기능
- 웹소설 메타데이터 관리 (제목, 작가, 장르, 줄거리)
- 작가 정보 관리
- 장르 및 분류 체계 관리
- 연재 정보 관리
- **평점/리뷰 시스템** (1-5점 평점, 텍스트 리뷰)
- **스포일러 관리** 및 모더레이션
- 리뷰 상호작용 (유용성 평가, 댓글)
- **사용자 신뢰도 관리**
- 검색 및 필터링 (Elasticsearch)
- 미디어 파일 관리 (표지 이미지)

### 📊 관리 테이블
```sql
-- 웹소설 및 메타데이터
novels
authors
genres
tags
platforms
novel_genres (다대다)
novel_tags (다대다)
novel_platforms (다대다)

-- 평점/리뷰 시스템
user_ratings
user_reviews
review_comments
review_helpfulness
user_trust_scores

-- 신고 및 모더레이션
review_reports
```

### 🔗 외부 연동
- CDN 서비스 (이미지 저장)
- Elasticsearch (검색 엔진)
- 추천 시스템 (메타데이터 제공)

---

## 3️⃣ Analytics Service (행동 분석 + 추천 관리)

### 📋 담당 요구사항
- **user_behavior_tracking_requirements.md** (전체)
- **recommendation_system_requirements.md** (Spring Boot 부분만)

### 🎯 주요 기능
- **사용자 행동 데이터 수집** (10ms 이하 응답)
- 세션 관리 및 추적
- 상호작용 추적 (클릭, 뷰, 북마크 등)
- 검색 행동 분석
- **추천 효과 측정** (노출, 클릭, 전환율)
- **추천 결과 관리 및 캐싱**
- **추천 피드백 수집** (좋아요/싫어요)
- 실시간 분석 및 배치 분석
- 사용자 프로필 업데이트

### 📊 관리 테이블
```sql
-- 행동 추적
user_behavior_events
user_sessions
novel_view_logs
search_behavior_logs

-- 추천 관리 (Spring Boot 부분)
user_interactions
recommendation_tracking
recommendation_feedback
recommendations (결과 캐시)

-- 분석 데이터
user_profiles (요약 정보)
```

### 🔗 외부 연동
- Redis (실시간 세션, 캐싱)
- Message Queue (이벤트 스트리밍)
- **Recommendation Service** (Python FastAPI)
- 모니터링 시스템 (Prometheus)

---

## 4️⃣ Recommendation Service (Python FastAPI)

### 📋 담당 요구사항
- **recommendation_system_requirements.md** (AI/ML 부분만)

### 🎯 주요 기능
- **AI 추천 알고리즘 실행**
  - 협업 필터링 (사용자 기반, 아이템 기반, 매트릭스 팩토라이제이션)
  - 콘텐츠 기반 필터링 (장르, 태그, TF-IDF)
  - 하이브리드 추천
- **모델 학습 및 관리**
- **신규 사용자/작품 처리** (콜드 스타트 해결)
- **추천 다양성 보장**
- **온라인 학습** (실시간 피드백 반영)

### 📊 관리 데이터
```python
# 모델 관련 (PostgreSQL)
model_metadata
training_logs

# 임베딩 및 유사도 (Redis/메모리)
user_embeddings
item_embeddings
similarity_matrices

# 실시간 캐시 (Redis)
user_recommendations_cache
item_similarity_cache
```

### 🔗 외부 연동
- **Analytics Service** (행동 데이터 수신, 추천 결과 전송)
- **User Service** (선호도 데이터 조회)
- **Content Service** (메타데이터 조회)
- Redis (캐싱)
- ML 라이브러리 (scikit-learn, TensorFlow)

---

## 🔄 서비스 간 데이터 흐름

### 📈 추천 생성 플로우
```
1. User Service → 선호도 데이터 → Recommendation Service
2. Content Service → 메타데이터 → Recommendation Service  
3. Analytics Service → 행동 데이터 → Recommendation Service
4. Recommendation Service → 추천 결과 → Analytics Service
5. Analytics Service → 캐시된 추천 → User/Frontend
```

### 📊 피드백 학습 플로우
```
1. Frontend → 사용자 행동 → Analytics Service
2. Analytics Service → 행동 분석 → User Service (선호도 업데이트)
3. Analytics Service → 피드백 데이터 → Recommendation Service
4. Recommendation Service → 모델 재학습 → 개선된 추천
```

### 🎯 핵심 API 통신
```
User Service ↔ Analytics Service (선호도 업데이트)
Content Service ↔ Analytics Service (메타데이터 동기화)
Analytics Service ↔ Recommendation Service (추천 요청/결과)
```

# Docker 환경 가이드

## 📋 구성된 Docker 파일들

### 1. **docker-compose.yml** - 기본 인프라
- PostgreSQL 15 (포트: 5432)
- Redis 7 (포트: 6379)  
- PgAdmin (포트: 5050) - DB 관리 도구 (선택적)

### 2. **docker-compose.dev.yml** - 개발 환경
- 기본 인프라 + 애플리케이션 서비스들
- 개발용 설정 및 볼륨 마운트

### 3. **docker-compose.prod.yml** - 운영 환경
- 보안 강화 및 리소스 제한
- Nginx 리버스 프록시 포함

## 🎛️ 서비스 옵션

### `infra` - 기본 구성 (추천)
- ✅ PostgreSQL + Redis만 실행
- ✅ 빠른 시작, 적은 리소스 사용
- ✅ 개발용으로 충분

### `infra-full` - 전체 구성
- ✅ PostgreSQL + Redis + PgAdmin
- ✅ 웹 기반 DB 관리 도구 포함
- ❌ 약간 더 많은 리소스 사용

## 🚀 빠른 시작

### 방법 1: PowerShell 스크립트 (한글 출력 최적화 - 추천)
```powershell
# 기본 구성 (PostgreSQL + Redis)
cd docker
.\setup-docker.ps1 infra

# 전체 구성 (PostgreSQL + Redis + PgAdmin)
cd docker
.\setup-docker.ps1 infra-full
```

### 방법 2: 배치 파일 (한글 출력 문제 해결됨)
```bash
# 기본 구성 (PostgreSQL + Redis)
cd docker
setup-docker.bat infra

# 전체 구성 (PostgreSQL + Redis + PgAdmin)
cd docker
setup-docker.bat infra-full
```

### 방법 3: 수동으로 시작
```bash
cd docker
docker-compose up -d
```

## 💡 한글 출력 문제 해결

### 문제 증상
- Windows 명령 프롬프트에서 한글이 깨져서 보임
- `???` 또는 이상한 문자로 표시됨

### 해결 방법

#### 1. PowerShell 사용 (가장 추천)
```powershell
# 기본 구성으로 시작
cd B:\workspace\webnovel-compass\docker
.\setup-docker.ps1 infra

# 또는 PgAdmin 포함한 전체 구성
.\setup-docker.ps1 infra-full
```

#### 2. 명령 프롬프트 인코딩 수정
```cmd
# 명령 프롬프트에서 UTF-8로 변경
chcp 65001

# 그 다음 배치 파일 실행
setup-docker.bat infra
```

#### 3. Windows Terminal 사용
- Windows Terminal을 설치하여 사용하면 한글 출력이 완벽하게 지원됩니다
- Microsoft Store에서 "Windows Terminal" 검색 후 설치

## 📊 접속 정보

### PostgreSQL
- **Host**: localhost
- **Port**: 5432
- **Database**: webnovel_compass
- **Username**: webnovel_user
- **Password**: webnovel_password

### Redis
- **Host**: localhost
- **Port**: 6379
- **Password**: (없음)

### PgAdmin (DB 관리도구)
- **URL**: http://localhost:5050
- **Email**: admin@webnovelcompass.com
- **Password**: admin123

## 🔧 유용한 명령어

### 서비스 상태 확인
```bash
docker-compose ps
```

### 로그 확인
```bash
# 전체 로그
docker-compose logs

# 특정 서비스 로그
docker-compose logs postgres
docker-compose logs redis
```

### 컨테이너 접속
```bash
# PostgreSQL 접속
docker exec -it webnovel-compass-db psql -U webnovel_user -d webnovel_compass

# Redis 접속
docker exec -it webnovel-compass-cache redis-cli
```

### 환경 정리
```bash
# 컨테이너 중지 및 제거
docker-compose down

# 볼륨까지 제거 (데이터 삭제됨!)
docker-compose down -v
```

## 📝 PgAdmin 설정

1. http://localhost:5050 접속
2. admin@webnovelcompass.com / admin123 로 로그인
3. 서버 추가:
   - **Name**: WebNovel Compass DB
   - **Host**: postgres (컨테이너명)
   - **Port**: 5432
   - **Database**: webnovel_compass
   - **Username**: webnovel_user
   - **Password**: webnovel_password

## 🐛 문제 해결

### PostgreSQL 연결 실패
```bash
# 컨테이너 재시작
docker-compose restart postgres

# 로그 확인
docker-compose logs postgres
```

### 포트 충돌
- 기본 포트를 변경하려면 .env 파일 수정
- 다른 PostgreSQL/Redis 서비스 중지 필요

### 볼륨 권한 문제 (Linux/Mac)
```bash
# 볼륨 권한 수정
sudo chown -R $USER:$USER postgres_data redis_data
```

## 🔄 다음 단계

1. **데이터베이스 스키마 생성**
   - database/init/ 폴더에 SQL 파일 추가
   - 컨테이너 재시작 시 자동 실행

2. **애플리케이션 서비스 추가**
   - Backend, Recommender 서비스 Dockerfile 작성
   - docker-compose.dev.yml에서 주석 해제

3. **환경변수 관리**
   - config/.env 파일 값 수정
   - 보안 키 설정

Docker 환경이 준비되었습니다! 🎉

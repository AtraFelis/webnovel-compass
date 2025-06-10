@echo off
REM 웹소설나침반 Docker 환경 설정 배치 파일 (Windows용)
REM 사용법: setup-docker.bat [옵션]

setlocal enabledelayedexpansion

REM 색상 설정을 위한 변수
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "NC=[0m"

REM 로그 함수들을 위한 라벨
goto :main

:log_info
echo %BLUE%[INFO]%NC% %~1
goto :eof

:log_success
echo %GREEN%[SUCCESS]%NC% %~1
goto :eof

:log_warning
echo %YELLOW%[WARNING]%NC% %~1
goto :eof

:log_error
echo %RED%[ERROR]%NC% %~1
goto :eof

REM Docker 및 Docker Compose 설치 확인
:check_dependencies
call :log_info "Docker 환경 확인 중..."

docker --version >nul 2>&1
if errorlevel 1 (
    call :log_error "Docker가 설치되지 않았습니다. https://docs.docker.com/get-docker/ 에서 설치해주세요."
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    call :log_error "Docker Compose가 설치되지 않았습니다."
    exit /b 1
)

call :log_success "Docker 환경 확인 완료"
goto :eof

REM 환경변수 파일 생성
:setup_env_file
call :log_info "환경변수 파일 설정 중..."

if not exist "..\config\.env" (
    copy "..\config\.env.template" "..\config\.env" >nul
    call :log_success ".env 파일이 생성되었습니다. 필요시 값을 수정해주세요."
) else (
    call :log_warning ".env 파일이 이미 존재합니다."
)
goto :eof

REM 네트워크 생성
:create_network
call :log_info "Docker 네트워크 생성 중..."

docker network ls | findstr "webnovel-network" >nul
if errorlevel 1 (
    docker network create webnovel-network
    call :log_success "webnovel-network 네트워크가 생성되었습니다."
) else (
    call :log_warning "webnovel-network 네트워크가 이미 존재합니다."
)
goto :eof

REM 기본 인프라 서비스 시작
:start_infrastructure
call :log_info "기본 인프라 서비스 시작 중..."

docker-compose -f docker-compose.yml up -d postgres redis

call :log_info "PostgreSQL 준비 대기 중..."
timeout /t 10 /nobreak >nul

REM PostgreSQL 연결 테스트
docker exec webnovel-compass-db pg_isready -U webnovel_user -d webnovel_compass >nul 2>&1
if errorlevel 1 (
    call :log_error "PostgreSQL 연결에 실패했습니다."
    exit /b 1
) else (
    call :log_success "PostgreSQL이 준비되었습니다."
)

call :log_success "기본 인프라 서비스가 시작되었습니다."
goto :eof

REM 전체 개발 환경 시작
:start_dev_environment
call :log_info "전체 개발 환경 시작 중..."

docker-compose -f docker-compose.dev.yml up -d postgres redis

call :log_success "개발 환경이 시작되었습니다."
goto :eof

REM 서비스 상태 확인
:check_services
call :log_info "서비스 상태 확인 중..."

echo.
docker-compose -f docker-compose.yml ps
echo.

call :log_info "접속 정보:"
echo   - PostgreSQL: localhost:5432
echo   - Redis: localhost:6379
echo   - PgAdmin: http://localhost:5050 (admin@webnovelcompass.com / admin123)
goto :eof

REM 정리 함수
:cleanup
call :log_info "Docker 환경 정리 중..."

docker-compose -f docker-compose.yml down -v
docker-compose -f docker-compose.dev.yml down -v

call :log_success "Docker 환경이 정리되었습니다."
goto :eof

REM 도움말 출력
:show_help
echo 웹소설나침반 Docker 환경 설정 배치 파일
echo.
echo 사용법:
echo   %~nx0 [옵션]
echo.
echo 옵션:
echo   infra     기본 인프라만 시작 (PostgreSQL, Redis)
echo   dev       전체 개발 환경 시작
echo   status    서비스 상태 확인
echo   cleanup   모든 컨테이너 및 볼륨 정리
echo   help      이 도움말 출력
goto :eof

REM 메인 스크립트
:main
cd /d "%~dp0"

set "option=%~1"
if "%option%"=="" set "option=infra"

if "%option%"=="infra" (
    call :check_dependencies
    if errorlevel 1 exit /b 1
    call :setup_env_file
    call :create_network
    call :start_infrastructure
    if errorlevel 1 exit /b 1
    call :check_services
) else if "%option%"=="dev" (
    call :check_dependencies
    if errorlevel 1 exit /b 1
    call :setup_env_file
    call :create_network
    call :start_dev_environment
    call :check_services
) else if "%option%"=="status" (
    call :check_services
) else if "%option%"=="cleanup" (
    call :cleanup
) else if "%option%"=="help" (
    call :show_help
) else if "%option%"=="-h" (
    call :show_help
) else if "%option%"=="--help" (
    call :show_help
) else (
    call :log_error "알 수 없는 옵션: %option%"
    call :show_help
    exit /b 1
)

endlocal

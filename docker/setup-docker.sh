#!/bin/bash

# 웹소설나침반 Docker 환경 설정 스크립트
# 사용법: ./setup-docker.sh [옵션]

set -e

# 색상 설정
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 로그 함수들
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Docker 및 Docker Compose 설치 확인
check_dependencies() {
    log_info "Docker 환경 확인 중..."
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker가 설치되지 않았습니다. https://docs.docker.com/get-docker/ 에서 설치해주세요."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose가 설치되지 않았습니다."
        exit 1
    fi
    
    log_success "Docker 환경 확인 완료"
}

# 환경변수 파일 생성
setup_env_file() {
    log_info "환경변수 파일 설정 중..."
    
    if [ ! -f "../config/.env" ]; then
        cp ../config/.env.template ../config/.env
        log_success ".env 파일이 생성되었습니다. 필요시 값을 수정해주세요."
    else
        log_warning ".env 파일이 이미 존재합니다."
    fi
}

# 네트워크 생성
create_network() {
    log_info "Docker 네트워크 생성 중..."
    
    if ! docker network ls | grep -q "webnovel-network"; then
        docker network create webnovel-network
        log_success "webnovel-network 네트워크가 생성되었습니다."
    else
        log_warning "webnovel-network 네트워크가 이미 존재합니다."
    fi
}

# 기본 인프라 서비스 시작 (PostgreSQL, Redis)
start_infrastructure() {
    log_info "기본 인프라 서비스 시작 중..."
    
    docker-compose -f docker-compose.yml up -d postgres redis
    
    log_info "PostgreSQL 준비 대기 중..."
    sleep 10
    
    # PostgreSQL 연결 테스트
    if docker exec webnovel-compass-db pg_isready -U webnovel_user -d webnovel_compass; then
        log_success "PostgreSQL이 준비되었습니다."
    else
        log_error "PostgreSQL 연결에 실패했습니다."
        exit 1
    fi
    
    log_success "기본 인프라 서비스가 시작되었습니다."
}

# 전체 개발 환경 시작
start_dev_environment() {
    log_info "전체 개발 환경 시작 중..."
    
    docker-compose -f docker-compose.dev.yml up -d postgres redis
    
    log_success "개발 환경이 시작되었습니다."
}

# 서비스 상태 확인
check_services() {
    log_info "서비스 상태 확인 중..."
    
    echo ""
    docker-compose -f docker-compose.yml ps
    echo ""
    
    log_info "접속 정보:"
    echo "  - PostgreSQL: localhost:5432"
    echo "  - Redis: localhost:6379"
    echo "  - PgAdmin: http://localhost:5050 (admin@webnovelcompass.com / admin123)"
}

# 정리 함수
cleanup() {
    log_info "Docker 환경 정리 중..."
    
    docker-compose -f docker-compose.yml down -v
    docker-compose -f docker-compose.dev.yml down -v
    
    log_success "Docker 환경이 정리되었습니다."
}

# 도움말 출력
show_help() {
    echo "웹소설나침반 Docker 환경 설정 스크립트"
    echo ""
    echo "사용법:"
    echo "  $0 [옵션]"
    echo ""
    echo "옵션:"
    echo "  infra     기본 인프라만 시작 (PostgreSQL, Redis)"
    echo "  dev       전체 개발 환경 시작"
    echo "  status    서비스 상태 확인"
    echo "  cleanup   모든 컨테이너 및 볼륨 정리"
    echo "  help      이 도움말 출력"
}

# 메인 스크립트
main() {
    cd "$(dirname "$0")"
    
    case "${1:-infra}" in
        "infra")
            check_dependencies
            setup_env_file
            create_network
            start_infrastructure
            check_services
            ;;
        "dev")
            check_dependencies
            setup_env_file
            create_network
            start_dev_environment
            check_services
            ;;
        "status")
            check_services
            ;;
        "cleanup")
            cleanup
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            log_error "알 수 없는 옵션: $1"
            show_help
            exit 1
            ;;
    esac
}

main "$@"

# 웹소설나침반 Docker 환경 설정 PowerShell 스크립트
# 사용법: .\setup-docker.ps1 [옵션]

param(
    [Parameter(Position=0)]
    [ValidateSet("infra", "infra-full", "dev", "status", "cleanup", "help")]
    [string]$Option = "infra"
)

# UTF-8 인코딩 설정
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# 색상 출력 함수
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$ForegroundColor = "White"
    )
    Write-Host $Message -ForegroundColor $ForegroundColor
}

function Log-Info {
    param([string]$Message)
    Write-ColorOutput "[INFO] $Message" "Blue"
}

function Log-Success {
    param([string]$Message)
    Write-ColorOutput "[SUCCESS] $Message" "Green"
}

function Log-Warning {
    param([string]$Message)
    Write-ColorOutput "[WARNING] $Message" "Yellow"
}

function Log-Error {
    param([string]$Message)
    Write-ColorOutput "[ERROR] $Message" "Red"
}

# Docker 및 Docker Compose 설치 확인
function Test-Dependencies {
    Log-Info "Docker 환경 확인 중..."
    
    try {
        $null = docker --version
        Log-Success "Docker가 설치되어 있습니다."
    }
    catch {
        Log-Error "Docker가 설치되지 않았습니다. https://docs.docker.com/get-docker/ 에서 설치해주세요."
        return $false
    }
    
    try {
        $null = docker-compose --version
        Log-Success "Docker Compose가 설치되어 있습니다."
    }
    catch {
        Log-Error "Docker Compose가 설치되지 않았습니다."
        return $false
    }
    
    Log-Success "Docker 환경 확인 완료"
    return $true
}

# 환경변수 파일 생성
function Setup-EnvFile {
    Log-Info "환경변수 파일 설정 중..."
    
    $envPath = "..\config\.env"
    $templatePath = "..\config\.env.template"
    
    if (-not (Test-Path $envPath)) {
        if (Test-Path $templatePath) {
            Copy-Item $templatePath $envPath
            Log-Success ".env 파일이 생성되었습니다. 필요시 값을 수정해주세요."
        } else {
            Log-Warning ".env.template 파일을 찾을 수 없습니다."
        }
    } else {
        Log-Warning ".env 파일이 이미 존재합니다."
    }
}

# 네트워크 생성
function New-DockerNetwork {
    Log-Info "Docker 네트워크 생성 중..."
    
    $networks = docker network ls --format "{{.Name}}"
    if ($networks -notcontains "webnovel-network") {
        docker network create webnovel-network
        Log-Success "webnovel-network 네트워크가 생성되었습니다."
    } else {
        Log-Warning "webnovel-network 네트워크가 이미 존재합니다."
    }
}

# 기본 인프라 서비스 시작 (PostgreSQL + Redis)
function Start-Infrastructure {
    Log-Info "기본 인프라 서비스 시작 중..."
    
    docker-compose -f docker-compose.yml up -d postgres redis
    
    if ($LASTEXITCODE -ne 0) {
        Log-Error "서비스 시작에 실패했습니다."
        return $false
    }
    
    Log-Info "PostgreSQL 준비 대기 중..."
    Start-Sleep -Seconds 10
    
    # PostgreSQL 연결 테스트
    $pgReady = docker exec webnovel-compass-db pg_isready -U webnovel_user -d webnovel_compass
    if ($LASTEXITCODE -eq 0) {
        Log-Success "PostgreSQL이 준비되었습니다."
    } else {
        Log-Error "PostgreSQL 연결에 실패했습니다."
        return $false
    }
    
    Log-Success "기본 인프라 서비스가 시작되었습니다."
    return $true
}

# 전체 인프라 서비스 시작 (PostgreSQL + Redis + PgAdmin)
function Start-FullInfrastructure {
    Log-Info "전체 인프라 서비스 시작 중 (PgAdmin 포함)..."
    
    docker-compose -f docker-compose.yml up -d postgres redis pgadmin
    
    if ($LASTEXITCODE -ne 0) {
        Log-Error "서비스 시작에 실패했습니다."
        return $false
    }
    
    Log-Info "PostgreSQL 준비 대기 중..."
    Start-Sleep -Seconds 10
    
    # PostgreSQL 연결 테스트
    $pgReady = docker exec webnovel-compass-db pg_isready -U webnovel_user -d webnovel_compass
    if ($LASTEXITCODE -eq 0) {
        Log-Success "PostgreSQL이 준비되었습니다."
    } else {
        Log-Error "PostgreSQL 연결에 실패했습니다."
        return $false
    }
    
    Log-Info "PgAdmin 준비 대기 중..."
    Start-Sleep -Seconds 5
    
    Log-Success "전체 인프라 서비스가 시작되었습니다."
    return $true
}

# 전체 개발 환경 시작
function Start-DevEnvironment {
    Log-Info "전체 개발 환경 시작 중..."
    
    docker-compose -f docker-compose.dev.yml up -d postgres redis
    
    if ($LASTEXITCODE -eq 0) {
        Log-Success "개발 환경이 시작되었습니다."
        return $true
    } else {
        Log-Error "개발 환경 시작에 실패했습니다."
        return $false
    }
}

# 서비스 상태 확인
function Show-ServiceStatus {
    Log-Info "서비스 상태 확인 중..."
    
    Write-Host ""
    docker-compose -f docker-compose.yml ps
    Write-Host ""
    
    # 실행 중인 서비스 확인
    $runningServices = docker-compose -f docker-compose.yml ps --services --filter "status=running"
    
    Log-Info "접속 정보:"
    Write-Host "  - PostgreSQL: localhost:5432"
    Write-Host "  - Redis: localhost:6379"
    
    if ($runningServices -contains "pgadmin") {
        Write-Host "  - PgAdmin: http://localhost:5050 (admin@webnovelcompass.com / admin123)"
    } else {
        Write-Host "  - PgAdmin: 실행되지 않음 (infra-full 옵션으로 시작하면 사용 가능)"
    }
}

# 정리 함수
function Remove-DockerEnvironment {
    Log-Info "Docker 환경 정리 중..."
    
    docker-compose -f docker-compose.yml down -v
    docker-compose -f docker-compose.dev.yml down -v
    
    Log-Success "Docker 환경이 정리되었습니다."
}

# 도움말 출력
function Show-Help {
    Write-Host "웹소설나침반 Docker 환경 설정 PowerShell 스크립트"
    Write-Host ""
    Write-Host "사용법:"
    Write-Host "  .\setup-docker.ps1 [옵션]"
    Write-Host ""
    Write-Host "옵션:"
    Write-Host "  infra      기본 인프라만 시작 (PostgreSQL + Redis)"
    Write-Host "  infra-full 전체 인프라 시작 (PostgreSQL + Redis + PgAdmin)"
    Write-Host "  dev        전체 개발 환경 시작"
    Write-Host "  status     서비스 상태 확인"
    Write-Host "  cleanup    모든 컨테이너 및 볼륨 정리"
    Write-Host "  help       이 도움말 출력"
    Write-Host ""
    Write-Host "예시:"
    Write-Host "  .\setup-docker.ps1 infra      # 가벼운 구성 (추천)"
    Write-Host "  .\setup-docker.ps1 infra-full # DB 관리 도구 포함"
}

# 메인 실행부
try {
    # 현재 디렉토리를 스크립트 위치로 변경
    Set-Location $PSScriptRoot
    
    switch ($Option) {
        "infra" {
            if (-not (Test-Dependencies)) { exit 1 }
            Setup-EnvFile
            New-DockerNetwork
            if (-not (Start-Infrastructure)) { exit 1 }
            Show-ServiceStatus
        }
        "infra-full" {
            if (-not (Test-Dependencies)) { exit 1 }
            Setup-EnvFile
            New-DockerNetwork
            if (-not (Start-FullInfrastructure)) { exit 1 }
            Show-ServiceStatus
        }
        "dev" {
            if (-not (Test-Dependencies)) { exit 1 }
            Setup-EnvFile
            New-DockerNetwork
            if (-not (Start-DevEnvironment)) { exit 1 }
            Show-ServiceStatus
        }
        "status" {
            Show-ServiceStatus
        }
        "cleanup" {
            Remove-DockerEnvironment
        }
        "help" {
            Show-Help
        }
        default {
            Log-Error "알 수 없는 옵션: $Option"
            Show-Help
            exit 1
        }
    }
}
catch {
    Log-Error "스크립트 실행 중 오류가 발생했습니다: $($_.Exception.Message)"
    exit 1
}

Write-Host ""
Log-Success "스크립트 실행이 완료되었습니다."
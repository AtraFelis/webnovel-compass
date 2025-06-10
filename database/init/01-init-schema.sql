-- 웹소설나침반 데이터베이스 초기화 스크립트
-- PostgreSQL 컨테이너 시작 시 자동 실행됩니다

-- 확장 기능 설치
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 사용자 테이블
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    birth_year INTEGER,
    gender VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 웹소설 테이블
CREATE TABLE IF NOT EXISTS novels (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(100) NOT NULL,
    genre VARCHAR(50),
    description TEXT,
    tags TEXT[], -- 배열로 태그 저장
    status VARCHAR(20) DEFAULT 'ongoing', -- ongoing, completed, hiatus
    total_chapters INTEGER DEFAULT 0,
    average_rating DECIMAL(3,2) DEFAULT 0.0,
    rating_count INTEGER DEFAULT 0,
    view_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 사용자 평점 테이블
CREATE TABLE IF NOT EXISTS user_ratings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    novel_id INTEGER REFERENCES novels(id) ON DELETE CASCADE,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    review TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, novel_id)
);

-- 인덱스 생성
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_novels_genre ON novels(genre);
CREATE INDEX IF NOT EXISTS idx_novels_author ON novels(author);
CREATE INDEX IF NOT EXISTS idx_novels_rating ON novels(average_rating);
CREATE INDEX IF NOT EXISTS idx_user_ratings_user_id ON user_ratings(user_id);
CREATE INDEX IF NOT EXISTS idx_user_ratings_novel_id ON user_ratings(novel_id);
CREATE INDEX IF NOT EXISTS idx_user_ratings_rating ON user_ratings(rating);

-- 기본 데이터 삽입을 위한 댓글
COMMENT ON TABLE users IS '사용자 정보 테이블';
COMMENT ON TABLE novels IS '웹소설 메타데이터 테이블';
COMMENT ON TABLE user_ratings IS '사용자 평점 및 리뷰 테이블';

-- 성공 메시지
SELECT 'Database initialized successfully!' as message;

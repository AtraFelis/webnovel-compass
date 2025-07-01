// 웹소설 기본 타입 정의
export interface WebNovel {
  id: number;
  title: string;
  author: string;
  rating: number;
  platform: Platform;
  genre: string[];
  cover: string;
  aiReason: string;
}

// 플랫폼 타입
export type Platform = "kakao" | "naver" | "munpia" | "novelpia" | "ridi";

// 플랫폼 정보
export interface PlatformInfo {
  name: string;
  color: string;
  logo: string;
  url: string;
}

// 화면 크기 타입
export type ScreenSize = "mobile" | "tablet" | "desktop";

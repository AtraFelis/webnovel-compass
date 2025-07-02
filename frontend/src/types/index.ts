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

// 앱 전역 상태 타입
export interface AppState {
  // 책 관련 상태
  books: WebNovel[];
  selectedBook: WebNovel | null;
  filteredBooks: WebNovel[];
  isLoading: boolean;
  
  // 검색 관련 상태
  searchQuery: string;
  
  // UI 상태
  currentPage: string;
}

// Context 타입
export interface AppContextType extends AppState {
  // 책 관련 액션
  setSelectedBook: (book: WebNovel | null) => void;
  selectBook: (book: WebNovel) => void;
  
  // 검색 관련 액션
  setSearchQuery: (query: string) => void;
  handleSearch: (query: string) => void;
  
  // UI 액션
  setCurrentPage: (page: string) => void;
}

import type { Platform, PlatformInfo } from "@/types";

// 플랫폼 정보 매핑
export const PLATFORMS: Record<Platform, PlatformInfo> = {
  kakao: {
    name: "카카오페이지",
    color: "#FFE812",
    logo: "/assets/platform-logos/kakao-page.png",
    url: "https://page.kakao.com",
  },
  naver: {
    name: "네이버시리즈",
    color: "#03C75A",
    logo: "/assets/platform-logos/naver-series.png",
    url: "https://series.naver.com",
  },
  munpia: {
    name: "문피아",
    color: "#4A90E2",
    logo: "/assets/platform-logos/munpia.png",
    url: "https://www.munpia.com",
  },
  novelpia: {
    name: "노벨피아",
    color: "#E94560",
    logo: "/assets/platform-logos/novelpia.png",
    url: "https://novelpia.com",
  },
  ridi: {
    name: "리디북스",
    color: "#1F8CE6",
    logo: "/assets/platform-logos/ridi.png",
    url: "https://ridibooks.com",
  },
};

// 더미 데이터 (MVP에서 사용)
export const mockBooks = [
  {
    id: 1,
    title: "전지적 독자 시점",
    author: "싱숑",
    rating: 4.9,
    platform: "naver" as Platform,
    genre: ["판타지", "현대"],
    cover:
      "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=300&h=400&fit=crop",
    aiReason: "메타픽션을 좋아하는 당신에게 완벽한 작품",
  },
  {
    id: 2,
    title: "달빛 조각사",
    author: "남희성",
    rating: 4.8,
    platform: "kakao" as Platform,
    genre: ["판타지", "게임"],
    cover:
      "https://page-images.kakaoentcdn.com/download/resource?kid=bfZSL7/hyqE7FmCzH/zJmsJkOYaJ0v8yAKjICsW1&filename=o1/dims/resize/384",
    aiReason: "게임 판타지의 흥미진진한 세계가 당신을 기다립니다",
  },
  {
    id: 3,
    title: "나 혼자만 레벨업",
    author: "추공",
    rating: 4.7,
    platform: "kakao" as Platform,
    genre: ["판타지", "액션"],
    cover:
      "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=300&h=400&fit=crop",
    aiReason: "성장형 주인공을 사랑하는 당신의 취향에 딱 맞아요",
  },
  {
    id: 4,
    title: "김부장",
    author: "정종원",
    rating: 4.6,
    platform: "munpia" as Platform,
    genre: ["현대", "드라마"],
    cover:
      "https://images.unsplash.com/photo-1532012197267-da84d127e765?w=300&h=400&fit=crop",
    aiReason: "현실적 스토리를 선호하는 당신을 위한 선택",
  },
  {
    id: 5,
    title: "마법사의 귀환",
    author: "유진성",
    rating: 4.8,
    platform: "ridi" as Platform,
    genre: ["판타지", "마법"],
    cover:
      "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=300&h=400&fit=crop",
    aiReason: "마법과 모험을 사랑하는 당신에게 추천하는 작품",
  },
  {
    id: 6,
    title: "회귀한 암살자",
    author: "이강민",
    rating: 4.7,
    platform: "novelpia" as Platform,
    genre: ["액션", "스릴러"],
    cover:
      "https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=300&h=400&fit=crop",
    aiReason: "긴장감 넘치는 액션을 좋아하는 당신을 위한 선택",
  },
  {
    id: 7,
    title: "천재 연금술사",
    author: "박소연",
    rating: 4.5,
    platform: "kakao" as Platform,
    genre: ["판타지", "연금술"],
    cover:
      "https://images.unsplash.com/photo-1577985051167-0d49eec21dd4?w=300&h=400&fit=crop",
    aiReason: "크래프팅과 성장 요소를 즐기는 독자에게 완벽",
  },
  {
    id: 8,
    title: "로맨스 판타지 아카데미",
    author: "최하늘",
    rating: 4.9,
    platform: "naver" as Platform,
    genre: ["로맨스", "판타지", "학원"],
    cover:
      "https://images.unsplash.com/photo-1519904981063-b0cf448d479e?w=300&h=400&fit=crop",
    aiReason: "달콤한 로맨스와 판타지의 조화가 매력적인 작품",
  },
  {
    id: 9,
    title: "무림고수 현대 적응기",
    author: "강철수",
    rating: 4.6,
    platform: "munpia" as Platform,
    genre: ["무협", "현대", "코미디"],
    cover:
      "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300&h=400&fit=crop",
    aiReason: "전통 무협과 현대의 재미있는 만남을 원하는 당신께",
  },
  {
    id: 10,
    title: "미래 전쟁 로봇",
    author: "김테크",
    rating: 4.4,
    platform: "ridi" as Platform,
    genre: ["SF", "메카", "액션"],
    cover:
      "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=300&h=400&fit=crop",
    aiReason: "SF와 메카닉 액션을 사랑하는 독자를 위한 작품",
  },
  {
    id: 11,
    title: "요리의 신",
    author: "이맛좋",
    rating: 4.7,
    platform: "novelpia" as Platform,
    genre: ["요리", "성장", "현대"],
    cover:
      "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=300&h=400&fit=crop",
    aiReason: "요리와 성장 스토리를 좋아하는 당신의 취향 저격",
  },
  {
    id: 12,
    title: "던전 경영 시뮬레이션",
    author: "박경영",
    rating: 4.8,
    platform: "kakao" as Platform,
    genre: ["판타지", "경영", "게임"],
    cover:
      "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=300&h=400&fit=crop",
    aiReason: "경영 시뮬레이션과 판타지의 완벽한 조합",
  },
];

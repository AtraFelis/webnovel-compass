# 웹소설나침반 React 프로젝트 이전 계획 🚀

## 📋 개요

Claude Artifact MVP → Vite + React + TypeScript 실제 프로젝트로 체계적 이전

## 🎯 적용할 개발 원칙

1. **컴포넌트화** - Atomic Design 패턴 적용
2. **DRY** - 공통 로직 훅/유틸로 분리
3. **KISS** - 단순하고 명확한 코드 구조
4. **단방향 데이터 흐름** - Props down, Events up
5. **상태 관리** - Context API 활용
6. **UI/UX 일관성** - 커스텀 디자인 시스템
7. **성능 최적화** - React.memo, 코드 스플리팅
8. **접근성** - ARIA, 키보드 네비게이션
9. **반응형** - Tailwind CSS 미디어 쿼리

---

## 📁 Phase 1: 프로젝트 설정 및 구조 확립

### 1.1 현재 프로젝트 상태 확인

```bash
cd B:\workspace\webnovel-compass\frontend
npm list  # 설치된 패키지 확인
```

### 1.2 필요한 패키지 추가 설치

```bash
# UI/UX 관련
npm install @heroicons/react lucide-react clsx

# 상태 관리 (선택사항)
npm install zustand  # 또는 Context API만 사용

# 개발 도구
npm install -D @types/react @types/react-dom
npm install -D eslint-plugin-jsx-a11y  # 접근성 검사
```

### 1.3 Tailwind CSS 설정 완료

```javascript
// tailwind.config.js 업데이트
/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        jakarta: ["Plus Jakarta Sans", "sans-serif"],
        noto: ["Noto Sans KR", "sans-serif"],
      },
      colors: {
        primary: "#6366f1", // 인디고
        secondary: "#8b5cf6", // 바이올렛
        accent: "#ec4899", // 핑크
      },
      animation: {
        float: "float 3s ease-in-out infinite",
        sparkle: "sparkle 2s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};
```

### 1.4 폴더 구조 생성

```
src/
├── components/
│   ├── atoms/           # 최소 단위 컴포넌트
│   │   ├── Button/
│   │   ├── Input/
│   │   ├── Icon/
│   │   └── LoadingSpinner/
│   ├── molecules/       # 원자 조합 컴포넌트
│   │   ├── SearchBar/
│   │   ├── RatingDisplay/
│   │   ├── GenreTagList/
│   │   └── AIBadge/
│   ├── organisms/       # 복합 컴포넌트
│   │   ├── Header/
│   │   ├── HeroSection/
│   │   ├── BookCard/
│   │   ├── BookGrid/
│   │   └── Navigation/
│   └── templates/       # 레이아웃 템플릿
│       ├── AppLayout/
│       └── ModalLayout/
├── pages/              # 페이지 컴포넌트
│   ├── HomePage/
│   ├── LibraryPage/
│   ├── SearchPage/
│   └── ProfilePage/
├── hooks/              # 커스텀 훅
│   ├── useScreenSize.ts
│   ├── useBooks.ts
│   └── useSearch.ts
├── contexts/           # Context API
│   ├── AppContext.tsx
│   └── BookContext.tsx
├── types/              # TypeScript 타입 정의
│   ├── book.ts
│   ├── user.ts
│   └── common.ts
├── utils/              # 유틸리티 함수
│   ├── constants.ts
│   └── helpers.ts
├── assets/             # 정적 자산
│   ├── images/
│   └── icons/
└── styles/             # 전역 스타일
    └── globals.css
```

---

## 🧱 Phase 2: 타입 정의 및 기본 구조

### 2.1 핵심 타입 정의

```typescript
// src/types/book.ts
export interface WebNovel {
  id: number;
  title: string;
  author: string;
  rating: number;
  platform: Platform;
  genre: string[];
  coverImage: string;
  aiRecommendReason: string;
  isCompleted: boolean;
}

export type Platform = "kakao" | "naver" | "munpia" | "novelpia" | "ridi";

export interface PlatformInfo {
  name: string;
  color: string;
  logo: string;
}

// src/types/common.ts
export interface AppState {
  currentPage: string;
  searchTerm: string;
  selectedBook: WebNovel | null;
  isLoading: boolean;
  books: WebNovel[];
}

export type ScreenSize = "mobile" | "tablet" | "desktop";
```

### 2.2 상수 정의

```typescript
// src/utils/constants.ts
export const PLATFORMS: Record<Platform, PlatformInfo> = {
  kakao: {
    name: "카카오페이지",
    color: "#FFE812",
    logo: "/platform-logos/kakao-page.png",
  },
  naver: {
    name: "네이버시리즈",
    color: "#03C75A",
    logo: "/platform-logos/naver-series.png",
  },
  munpia: {
    name: "문피아",
    color: "#4A90E2",
    logo: "/platform-logos/munpia.png",
  },
  novelpia: {
    name: "노벨피아",
    color: "#E94560",
    logo: "/platform-logos/novelpia.png",
  },
  ridi: {
    name: "리디북스",
    color: "#1F8CE6",
    logo: "/platform-logos/ridi.png",
  },
};

export const BREAKPOINTS = {
  mobile: 768,
  tablet: 1024,
  desktop: 1280,
} as const;

export const NAVIGATION_ITEMS = [
  { icon: "Home", label: "Home", id: "home" },
  { icon: "BookOpen", label: "Library", id: "library" },
  { icon: "Search", label: "Search", id: "search" },
  { icon: "User", label: "Profile", id: "profile" },
] as const;
```

---

## ⚛️ Phase 3: Atomic Design 컴포넌트 구현

### 3.1 Atoms (원자) - 최소 단위 컴포넌트

#### Button 컴포넌트

```typescript
// src/components/atoms/Button/Button.tsx
interface ButtonProps {
  variant: "primary" | "secondary" | "ghost";
  size: "sm" | "md" | "lg";
  children: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  className?: string;
}

export const Button: React.FC<ButtonProps> = ({
  variant,
  size,
  children,
  onClick,
  disabled,
  className,
}) => {
  const baseClasses =
    "font-bold rounded-full transition-all transform hover:scale-105";
  const variantClasses = {
    primary: "bg-gradient-to-r from-purple-500 to-pink-500 text-white",
    secondary: "bg-purple-100 text-purple-700 hover:bg-purple-200",
    ghost: "text-purple-600 hover:bg-purple-50",
  };
  const sizeClasses = {
    sm: "px-4 py-2 text-sm",
    md: "px-6 py-3 text-base",
    lg: "px-8 py-4 text-lg",
  };

  return (
    <button
      className={clsx(
        baseClasses,
        variantClasses[variant],
        sizeClasses[size],
        className
      )}
      onClick={onClick}
      disabled={disabled}
      aria-label={typeof children === "string" ? children : undefined}
    >
      {children}
    </button>
  );
};
```

#### LoadingSpinner 컴포넌트

```typescript
// src/components/atoms/LoadingSpinner/LoadingSpinner.tsx
interface LoadingSpinnerProps {
  size?: "sm" | "md" | "lg";
  message?: string;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = "md",
  message = "로딩 중...",
}) => {
  const sizeClasses = {
    sm: "w-16 h-16",
    md: "w-24 h-24",
    lg: "w-32 h-32",
  };

  return (
    <div
      className="flex flex-col items-center justify-center"
      role="status"
      aria-live="polite"
    >
      <div className={`relative ${sizeClasses[size]} mx-auto mb-4`}>
        <div className="absolute inset-0 border-4 border-purple-200 rounded-full animate-spin" />
        <div
          className="absolute inset-2 border-4 border-purple-400 rounded-full animate-spin"
          style={{ animationDirection: "reverse" }}
        />
        <div className="absolute inset-4 border-4 border-purple-600 rounded-full animate-spin" />
        <Compass className="absolute inset-0 m-auto w-8 h-8 text-purple-600 animate-pulse" />
      </div>
      <p className="text-purple-700 font-semibold">{message}</p>
    </div>
  );
};
```

### 3.2 Molecules (분자) - 원자 조합

#### SearchBar 컴포넌트

```typescript
// src/components/molecules/SearchBar/SearchBar.tsx
interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  placeholder?: string;
}

export const SearchBar: React.FC<SearchBarProps> = ({
  value,
  onChange,
  onSubmit,
  placeholder = "어떤 이야기를 찾으시나요?",
}) => {
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      onSubmit();
    }
  };

  return (
    <div className="relative max-w-4xl mx-auto">
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder={placeholder}
        className="w-full bg-white/80 border-2 border-purple-200 rounded-full px-4 py-3 lg:py-4 pl-12 lg:pl-14 text-gray-800 placeholder-purple-400 focus:outline-none focus:border-purple-400 backdrop-blur-sm shadow-md text-base lg:text-lg"
        aria-label="웹소설 검색"
      />
      <Search className="absolute left-4 lg:left-5 top-1/2 transform -translate-y-1/2 w-5 h-5 lg:w-6 lg:h-6 text-purple-500" />
      <button
        onClick={onSubmit}
        className="absolute right-3 lg:right-4 top-1/2 transform -translate-y-1/2"
        aria-label="검색하기"
      >
        <Sparkles className="w-5 h-5 lg:w-6 lg:h-6 text-purple-500 animate-pulse" />
      </button>
    </div>
  );
};
```

#### RatingDisplay 컴포넌트

```typescript
// src/components/molecules/RatingDisplay/RatingDisplay.tsx
interface RatingDisplayProps {
  rating: number;
  maxRating?: number;
  size?: "sm" | "md" | "lg";
  showNumber?: boolean;
}

export const RatingDisplay: React.FC<RatingDisplayProps> = ({
  rating,
  maxRating = 5,
  size = "md",
  showNumber = true,
}) => {
  const sizeClasses = {
    sm: "w-3 h-3",
    md: "w-4 h-4",
    lg: "w-5 h-5",
  };

  return (
    <div
      className="flex items-center gap-1"
      role="img"
      aria-label={`${rating}점 만점에 ${rating}점`}
    >
      {[...Array(maxRating)].map((_, i) => (
        <Star
          key={i}
          className={`${sizeClasses[size]} ${
            i < Math.floor(rating)
              ? "text-yellow-500 fill-current"
              : "text-gray-300"
          }`}
        />
      ))}
      {showNumber && (
        <span
          className={`text-yellow-600 ml-1 font-medium ${
            size === "sm" ? "text-xs" : size === "lg" ? "text-base" : "text-sm"
          }`}
        >
          ({rating})
        </span>
      )}
    </div>
  );
};
```

### 3.3 Organisms (유기체) - 복합 컴포넌트

#### BookCard 컴포넌트

```typescript
// src/components/organisms/BookCard/BookCard.tsx
interface BookCardProps {
  book: WebNovel;
  onClick: (book: WebNovel) => void;
  size?: "sm" | "md" | "lg";
}

export const BookCard: React.FC<BookCardProps> = ({
  book,
  onClick,
  size = "md",
}) => {
  const sizeClasses = {
    sm: { card: "p-3", image: "h-32", title: "text-sm", author: "text-xs" },
    md: { card: "p-4", image: "h-40", title: "text-base", author: "text-sm" },
    lg: { card: "p-4", image: "h-48", title: "text-lg", author: "text-base" },
  };

  return (
    <article
      className={`relative bg-white/80 backdrop-blur-sm rounded-xl border-2 border-purple-200 hover:border-purple-400 cursor-pointer transition-all duration-300 hover:transform hover:scale-105 hover:shadow-xl hover:shadow-purple-200/50 ${sizeClasses[size].card}`}
      onClick={() => onClick(book)}
      role="button"
      tabIndex={0}
      onKeyPress={(e) => (e.key === "Enter" || e.key === " ") && onClick(book)}
      aria-label={`${book.title} - ${book.author} 작품 상세보기`}
    >
      {/* 글로우 효과 */}
      <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-purple-100/50 to-pink-100/50 opacity-0 hover:opacity-100 transition-opacity duration-300" />

      <div className="relative z-10">
        {/* 책 표지 */}
        <div className="relative mb-3">
          <img
            src={book.coverImage}
            alt={`${book.title} 표지`}
            className={`w-full ${sizeClasses[size].image} object-cover rounded-lg`}
            loading="lazy"
          />

          {/* AI 추천 배지 */}
          <AIBadge className="absolute -top-2 -right-2" />

          {/* 플랫폼 배지 */}
          <PlatformBadge
            platform={book.platform}
            className="absolute bottom-2 right-2"
          />
        </div>

        {/* 책 정보 */}
        <h3
          className={`text-gray-800 font-bold mb-1 line-clamp-2 ${sizeClasses[size].title}`}
        >
          {book.title}
        </h3>
        <p className={`text-purple-600 mb-2 ${sizeClasses[size].author}`}>
          {book.author}
        </p>

        {/* 평점 */}
        <RatingDisplay
          rating={book.rating}
          size={size === "lg" ? "md" : "sm"}
        />

        {/* 장르 태그 */}
        <GenreTagList genres={book.genre} size={size} />
      </div>
    </article>
  );
};
```

---

## 🏗️ Phase 4: 상태 관리 구현

### 4.1 Context API 설정

```typescript
// src/contexts/AppContext.tsx
interface AppContextType {
  currentPage: string;
  setCurrentPage: (page: string) => void;
  searchTerm: string;
  setSearchTerm: (term: string) => void;
  selectedBook: WebNovel | null;
  setSelectedBook: (book: WebNovel | null) => void;
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const AppProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [currentPage, setCurrentPage] = useState("home");
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedBook, setSelectedBook] = useState<WebNovel | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  return (
    <AppContext.Provider
      value={{
        currentPage,
        setCurrentPage,
        searchTerm,
        setSearchTerm,
        selectedBook,
        setSelectedBook,
        isLoading,
        setIsLoading,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

export const useAppContext = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error("useAppContext must be used within AppProvider");
  }
  return context;
};
```

### 4.2 커스텀 훅

```typescript
// src/hooks/useScreenSize.ts
export const useScreenSize = (): ScreenSize => {
  const [screenSize, setScreenSize] = useState<ScreenSize>("mobile");

  useEffect(() => {
    const updateScreenSize = () => {
      const width = window.innerWidth;
      if (width >= BREAKPOINTS.desktop) {
        setScreenSize("desktop");
      } else if (width >= BREAKPOINTS.tablet) {
        setScreenSize("tablet");
      } else {
        setScreenSize("mobile");
      }
    };

    updateScreenSize();
    window.addEventListener("resize", updateScreenSize);
    return () => window.removeEventListener("resize", updateScreenSize);
  }, []);

  return screenSize;
};

// src/hooks/useBooks.ts
export const useBooks = () => {
  const [books, setBooks] = useState<WebNovel[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchBooks = useCallback(async (filters?: BookFilters) => {
    setLoading(true);
    setError(null);

    try {
      // API 호출 로직
      const response = await fetch("/api/books", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(filters),
      });

      if (!response.ok) throw new Error("Failed to fetch books");

      const data = await response.json();
      setBooks(data.books);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }, []);

  return { books, loading, error, fetchBooks };
};
```

---

## 📄 Phase 5: 페이지 구현

### 5.1 HomePage 구현

```typescript
// src/pages/HomePage/HomePage.tsx
export const HomePage: React.FC = () => {
  const {
    searchTerm,
    setSearchTerm,
    setSelectedBook,
    isLoading,
    setIsLoading,
  } = useAppContext();
  const { books, fetchBooks } = useBooks();
  const screenSize = useScreenSize();

  const handleSearch = useCallback(() => {
    if (!searchTerm.trim()) return;

    setIsLoading(true);
    fetchBooks({ search: searchTerm });
  }, [searchTerm, fetchBooks, setIsLoading]);

  const handleBookClick = useCallback(
    (book: WebNovel) => {
      setSelectedBook(book);
    },
    [setSelectedBook]
  );

  // 초기 데이터 로드
  useEffect(() => {
    fetchBooks();
  }, [fetchBooks]);

  if (isLoading) {
    return (
      <AppLayout>
        <div className="flex items-center justify-center min-h-screen">
          <LoadingSpinner size="lg" message="취향 분석 중..." />
        </div>
      </AppLayout>
    );
  }

  return (
    <AppLayout>
      {/* 히어로 섹션 */}
      <HeroSection onSearchClick={handleSearch} />

      {/* 검색바 */}
      <div className="p-4 lg:p-6">
        <SearchBar
          value={searchTerm}
          onChange={setSearchTerm}
          onSubmit={handleSearch}
        />
      </div>

      {/* 추천 도서 */}
      <BookGrid
        books={books}
        onBookClick={handleBookClick}
        screenSize={screenSize}
      />
    </AppLayout>
  );
};
```

---

## 🚀 Phase 6: 성능 최적화 및 접근성

### 6.1 성능 최적화

```typescript
// React.memo로 불필요한 리렌더링 방지
export const BookCard = React.memo<BookCardProps>(
  ({ book, onClick, size }) => {
    // 컴포넌트 로직
  },
  (prevProps, nextProps) => {
    // 얕은 비교로 최적화
    return (
      prevProps.book.id === nextProps.book.id &&
      prevProps.size === nextProps.size
    );
  }
);

// useMemo로 비용이 큰 계산 최적화
const BookGrid: React.FC<BookGridProps> = ({
  books,
  onBookClick,
  screenSize,
}) => {
  const gridColumns = useMemo(() => {
    switch (screenSize) {
      case "desktop":
        return "grid-cols-5";
      case "tablet":
        return "grid-cols-3";
      default:
        return "grid-cols-2";
    }
  }, [screenSize]);

  const sortedBooks = useMemo(() => {
    return [...books].sort((a, b) => b.rating - a.rating);
  }, [books]);

  return (
    <div className={`grid gap-4 ${gridColumns}`}>
      {sortedBooks.map((book) => (
        <BookCard key={book.id} book={book} onClick={onBookClick} />
      ))}
    </div>
  );
};

// useCallback으로 함수 참조 안정화
const HomePage: React.FC = () => {
  const handleBookClick = useCallback(
    (book: WebNovel) => {
      setSelectedBook(book);
    },
    [setSelectedBook]
  );

  const handleSearch = useCallback(async () => {
    if (!searchTerm.trim()) return;
    await fetchBooks({ search: searchTerm });
  }, [searchTerm, fetchBooks]);
};

// 이미지 Lazy Loading
const LazyImage: React.FC<ImageProps> = ({ src, alt, className }) => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [isInView, setIsInView] = useState(false);
  const imgRef = useRef<HTMLImageElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsInView(true);
          observer.disconnect();
        }
      },
      { threshold: 0.1 }
    );

    if (imgRef.current) {
      observer.observe(imgRef.current);
    }

    return () => observer.disconnect();
  }, []);

  return (
    <div ref={imgRef} className={`bg-gray-200 ${className}`}>
      {isInView && (
        <img
          src={src}
          alt={alt}
          className={`${className} transition-opacity duration-300 ${
            isLoaded ? "opacity-100" : "opacity-0"
          }`}
          onLoad={() => setIsLoaded(true)}
          loading="lazy"
        />
      )}
    </div>
  );
};

// 코드 스플리팅
const LibraryPage = React.lazy(() => import("../pages/LibraryPage"));
const SearchPage = React.lazy(() => import("../pages/SearchPage"));
const ProfilePage = React.lazy(() => import("../pages/ProfilePage"));

// App.tsx에서 Suspense 사용
function App() {
  return (
    <AppProvider>
      <Router>
        <Suspense fallback={<LoadingSpinner size="lg" />}>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/library" element={<LibraryPage />} />
            <Route path="/search" element={<SearchPage />} />
            <Route path="/profile" element={<ProfilePage />} />
          </Routes>
        </Suspense>
      </Router>
    </AppProvider>
  );
}
```

### 6.2 접근성 개선

```typescript
// 키보드 네비게이션 지원
const BookCard: React.FC<BookCardProps> = ({ book, onClick }) => {
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      onClick(book);
    }
  };

  return (
    <article
      className="..."
      onClick={() => onClick(book)}
      onKeyPress={handleKeyPress}
      tabIndex={0}
      role="button"
      aria-label={`${book.title} - ${book.author} 작품 상세보기`}
    >
      {/* 콘텐츠 */}
    </article>
  );
};

// 스크린 리더 지원
const RatingDisplay: React.FC<RatingDisplayProps> = ({ rating, maxRating }) => {
  return (
    <div
      className="flex items-center gap-1"
      role="img"
      aria-label={`평점 ${maxRating}점 만점에 ${rating}점`}
    >
      {/* 별점 표시 */}
    </div>
  );
};

// Focus trap 모달
const Modal: React.FC<ModalProps> = ({ isOpen, onClose, children }) => {
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isOpen) {
      // 첫 번째 포커스 가능한 요소에 포커스
      const firstFocusable = modalRef.current?.querySelector(
        'button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      (firstFocusable as HTMLElement)?.focus();
    }
  }, [isOpen]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Escape") {
      onClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      <div
        ref={modalRef}
        className="bg-white rounded-lg p-6 max-w-md w-full mx-4"
        onKeyDown={handleKeyDown}
      >
        {children}
      </div>
    </div>
  );
};

// 색상 대비 확인 (WCAG 2.1 AA 기준)
const colorContrast = {
  // 최소 4.5:1 비율 유지
  primary: "#6366f1", // 충분한 대비
  text: "#1f2937", // 충분한 대비
  background: "#ffffff", // 충분한 대비
};
```

---

## 🧪 Phase 7: 테스트 구현

### 7.1 컴포넌트 테스트

```typescript
// src/components/atoms/Button/Button.test.tsx
import { render, screen, fireEvent } from "@testing-library/react";
import { Button } from "./Button";

describe("Button 컴포넌트", () => {
  test("기본 렌더링이 정상적으로 작동한다", () => {
    render(
      <Button variant="primary" size="md">
        테스트 버튼
      </Button>
    );
    expect(screen.getByRole("button")).toBeInTheDocument();
    expect(screen.getByText("테스트 버튼")).toBeInTheDocument();
  });

  test("클릭 이벤트가 정상적으로 작동한다", () => {
    const handleClick = jest.fn();
    render(
      <Button variant="primary" size="md" onClick={handleClick}>
        클릭 테스트
      </Button>
    );

    fireEvent.click(screen.getByRole("button"));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  test("disabled 상태일 때 클릭이 작동하지 않는다", () => {
    const handleClick = jest.fn();
    render(
      <Button variant="primary" size="md" onClick={handleClick} disabled>
        비활성화 버튼
      </Button>
    );

    fireEvent.click(screen.getByRole("button"));
    expect(handleClick).not.toHaveBeenCalled();
  });
});

// src/hooks/useScreenSize.test.ts
import { renderHook } from "@testing-library/react";
import { useScreenSize } from "./useScreenSize";

describe("useScreenSize 훅", () => {
  test("초기값이 올바르게 설정된다", () => {
    Object.defineProperty(window, "innerWidth", {
      writable: true,
      configurable: true,
      value: 320,
    });

    const { result } = renderHook(() => useScreenSize());
    expect(result.current).toBe("mobile");
  });
});
```

### 7.2 E2E 테스트 (Cypress)

```typescript
// cypress/e2e/homepage.cy.ts
describe("홈페이지 E2E 테스트", () => {
  beforeEach(() => {
    cy.visit("/");
  });

  it("홈페이지가 정상적으로 로드된다", () => {
    cy.contains("웹소설나침반").should("be.visible");
    cy.contains("당신을 위한 맞춤 추천").should("be.visible");
  });

  it("검색 기능이 정상적으로 작동한다", () => {
    cy.get('input[aria-label="웹소설 검색"]').type("전지적 독자 시점");
    cy.get('button[aria-label="검색하기"]').click();
    cy.contains("검색 결과").should("be.visible");
  });

  it("웹소설 카드 클릭 시 상세 모달이 열린다", () => {
    cy.get('[role="button"]').first().click();
    cy.get('[role="dialog"]').should("be.visible");
    cy.contains("AI의 추천 이유").should("be.visible");
  });

  it("네비게이션이 정상적으로 작동한다", () => {
    cy.get('[aria-label="Library 페이지로 이동"]').click();
    cy.url().should("include", "/library");
  });
});
```

---

## 📦 Phase 8: 빌드 최적화 및 배포 준비

### 8.1 Vite 설정 최적화

```typescript
// vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import path from "path";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      "@components": path.resolve(__dirname, "./src/components"),
      "@pages": path.resolve(__dirname, "./src/pages"),
      "@hooks": path.resolve(__dirname, "./src/hooks"),
      "@utils": path.resolve(__dirname, "./src/utils"),
      "@types": path.resolve(__dirname, "./src/types"),
    },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ["react", "react-dom"],
          router: ["react-router-dom"],
          icons: ["lucide-react", "@heroicons/react"],
        },
      },
    },
    sourcemap: process.env.NODE_ENV === "development",
  },
  server: {
    port: 3000,
    proxy: {
      "/api": {
        target: "http://localhost:8080",
        changeOrigin: true,
        secure: false,
      },
    },
  },
});
```

### 8.2 환경 설정

```bash
# .env.local
VITE_API_URL=http://localhost:8080/api
VITE_APP_TITLE=웹소설나침반
VITE_APP_VERSION=1.0.0

# .env.production
VITE_API_URL=https://api.webnovel-compass.com
VITE_APP_TITLE=웹소설나침반
VITE_APP_VERSION=1.0.0
```

### 8.3 Package.json 스크립트

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "test": "vitest",
    "test:e2e": "cypress open",
    "test:e2e:headless": "cypress run",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "lint:fix": "eslint . --ext ts,tsx --fix",
    "type-check": "tsc --noEmit",
    "format": "prettier --write \"src/**/*.{ts,tsx}\"",
    "analyze": "npx vite-bundle-analyzer"
  }
}
```

---

## 🎯 실행 체크리스트

### ✅ Phase 1: 프로젝트 설정

- [ ] 패키지 설치 확인
- [ ] Tailwind CSS 설정 완료
- [ ] 폴더 구조 생성
- [ ] 타입 정의 작성

### ✅ Phase 2: 컴포넌트 구현

- [ ] Atoms 컴포넌트 구현
- [ ] Molecules 컴포넌트 구현
- [ ] Organisms 컴포넌트 구현
- [ ] Templates 컴포넌트 구현

### ✅ Phase 3: 상태 관리

- [ ] Context API 설정
- [ ] 커스텀 훅 구현
- [ ] 전역 상태 연결

### ✅ Phase 4: 페이지 구현

- [ ] HomePage 구현
- [ ] 라우팅 설정
- [ ] 네비게이션 연결

### ✅ Phase 5: 최적화

- [ ] 성능 최적화 적용
- [ ] 접근성 개선
- [ ] 테스트 작성

### ✅ Phase 6: 배포 준비

- [ ] 빌드 최적화
- [ ] 환경 설정
- [ ] 문서 작성

---

## 🚀 시작하기

```bash
# 1. 프로젝트 디렉토리로 이동
cd B:\workspace\webnovel-compass\frontend

# 2. 현재 상태 확인
npm list
npm run dev  # 기본 설정 확인

# 3. 필요한 패키지 설치
npm install @heroicons/react lucide-react clsx

# 4. 첫 번째 컴포넌트 구현 시작
# src/types/book.ts 파일부터 생성!
```

이 계획을 단계별로 따라가시면, **체계적이고 확장 가능한 웹소설나침반**을 구축할 수 있습니다! 어떤 단계부터 시작하고 싶으신가요? 🎯

import React, {
  createContext,
  useContext,
  useState,
  useCallback,
  ReactNode,
} from "react";
import type { AppContextType, WebNovel } from "@/types";
import { mockBooks } from "@/utils/constants";

// Context 생성
const AppContext = createContext<AppContextType | undefined>(undefined);

// Provider Props 타입
interface AppProviderProps {
  children: ReactNode;
}

// AppProvider 컴포넌트
export const AppProvider: React.FC<AppProviderProps> = ({ children }) => {
  // 상태 정의
  const [books] = useState<WebNovel[]>(mockBooks);
  const [selectedBook, setSelectedBook] = useState<WebNovel | null>(null);
  const [filteredBooks, setFilteredBooks] = useState<WebNovel[]>(mockBooks);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [currentPage, setCurrentPage] = useState<string>("home");

  // 책 선택 액션
  const selectBook = useCallback((book: WebNovel) => {
    setSelectedBook(book);
    console.log("선택된 책:", book.title);
  }, []);

  // 검색 처리 액션
  const handleSearch = useCallback(
    (query: string) => {
      setSearchQuery(query);
      setIsLoading(true);

      // TODO: 실제로는 API 호출이지만, 현재는 필터링으로 시뮬레이션
      setTimeout(() => {
        if (query.trim() === "") {
          setFilteredBooks(books);
        } else {
          const filtered = books.filter(
            (book) =>
              book.title.toLowerCase().includes(query.toLowerCase()) ||
              book.author.toLowerCase().includes(query.toLowerCase()) ||
              book.genre.some((genre) =>
                genre.toLowerCase().includes(query.toLowerCase())
              )
          );
          setFilteredBooks(filtered);
        }
        setIsLoading(false);
      }, 300); // AI 검색 시뮬레이션
    },
    [books]
  );

  // Context 값 정의
  const contextValue: AppContextType = {
    // 상태
    books,
    selectedBook,
    filteredBooks,
    isLoading,
    searchQuery,
    currentPage,

    // 액션
    setSelectedBook,
    selectBook,
    setSearchQuery,
    handleSearch,
    setCurrentPage,
  };

  return (
    <AppContext.Provider value={contextValue}>{children}</AppContext.Provider>
  );
};

// Context 사용 훅
export const useAppContext = (): AppContextType => {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error("useAppContext must be used within an AppProvider");
  }
  return context;
};

export default AppContext;

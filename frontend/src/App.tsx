import React from "react";
import { AppProvider } from "./contexts/AppContext";
import { Header } from "./components/organisms/Header";
import { MobileNavigation } from "./components/organisms/Navigation";
import { SearchBar } from "./components/molecules/SearchBar";
import { HeroSection } from "./components/molecules/HeroSection";
import { BookCard } from "./components/organisms/BookCard";
import { MagicalStars } from "./components/atoms/MagicalStars";
import { BookDetailModal } from "./components/organisms/BookDetailModal";
import { useBooks, useSearch, useModal } from "./hooks";

// 메인 앱 컴포넌트 (Context 내부)
const AppContent: React.FC = () => {
  const { filteredBooks } = useBooks();
  const { handleSearch } = useSearch();
  const { openModal, isOpen, selectedBook, closeModal } = useModal();

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-100 via-purple-50 to-pink-100 relative overflow-hidden">
      {/* 마법적 별 배경 */}
      <MagicalStars />

      {/* 헤더 */}
      <Header />

      {/* 검색바 */}
      <div data-search-section>
        <SearchBar onSearch={handleSearch} />
      </div>
      
      {/* 히어로 섹션 */}
      <HeroSection />

      {/* 책 그리드 */}
      <div className="relative z-10 px-6 pb-8 md:pb-8 pb-20">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-2xl font-bold text-purple-700 mb-6 flex items-center gap-2">
            추천 도서
          </h2>

          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
            {filteredBooks.map((book) => (
              <BookCard key={book.id} book={book} onClick={openModal} />
            ))}
          </div>

          {/* 검색 결과 없음 */}
          {filteredBooks.length === 0 && (
            <div className="text-center py-12">
              <p className="text-purple-600 text-lg mb-2">
                🔍 검색 결과가 없습니다
              </p>
              <p className="text-purple-500 text-sm">
                다른 키워드로 검색해보세요
              </p>
            </div>
          )}
        </div>
      </div>

      {/* 책 상세 모달 */}
      <BookDetailModal
        book={selectedBook}
        isOpen={isOpen}
        onClose={closeModal}
      />
      
      {/* 모바일 하단 네비게이션 */}
      <MobileNavigation />
    </div>
  );
};

// 메인 App 컴포넌트 (Context Provider 포함)
function App() {
  return (
    <AppProvider>
      <AppContent />
    </AppProvider>
  );
}

export default App;

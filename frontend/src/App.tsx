import { useState } from "react";
import { Book } from "lucide-react";
import { Header } from "./components/organisms/Header";
import { SearchBar } from "./components/molecules/SearchBar";
import { MagicalBookCard } from "./components/organisms/BookCard";
import { MagicalStars } from "./components/atoms/MagicalStars";
import { BookDetailModal } from "./components/organisms/BookDetailModal";
import type { WebNovel } from "./types";
import { mockBooks } from "./utils/constants";

function App() {
  const [selectedBook, setSelectedBook] = useState<WebNovel | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [filteredBooks, setFilteredBooks] = useState(mockBooks);

  const handleBookClick = (book: WebNovel) => {
    setSelectedBook(book);
    console.log("클릭된 책:", book.title);
  };

  const handleSearch = (query: string) => {
    setSearchQuery(query);
    if (query.trim() === "") {
      setFilteredBooks(mockBooks);
    } else {
      const filtered = mockBooks.filter(
        (book) =>
          book.title.toLowerCase().includes(query.toLowerCase()) ||
          book.author.toLowerCase().includes(query.toLowerCase()) ||
          book.genre.some((genre) =>
            genre.toLowerCase().includes(query.toLowerCase())
          )
      );
      setFilteredBooks(filtered);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-100 via-purple-50 to-pink-100 relative overflow-hidden">
      {/* 마법적 별 배경 */}
      <MagicalStars />

      {/* 헤더 */}
      <Header />

      {/* 검색바 */}
      <SearchBar onSearch={handleSearch} />

      {/* 메인 콘텐츠 */}
      <main className="p-6">
        <div className="max-w-4xl mx-auto relative z-10">
          <h2 className="text-xl font-bold text-purple-700 mb-4">
            <Book className="w-5 h-5 lg:w-6 lg:h-6 mr-2 inline-block text-current" />
            {searchQuery
              ? `검색 결과 (${filteredBooks.length}개)`
              : "추천 웹소설"}
          </h2>
          {filteredBooks.length > 0 ? (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {filteredBooks.map((book) => (
                <MagicalBookCard
                  key={book.id}
                  book={book}
                  onClick={handleBookClick}
                />
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <div className="text-gray-400 text-lg mb-2">📚</div>
              <p className="text-gray-500 text-lg font-medium">
                검색 결과가 없습니다
              </p>
              <p className="text-gray-400 text-sm mt-2">
                다른 키워드로 검색해보세요
              </p>
            </div>
          )}
        </div>
      </main>

      {/* 책 상세 모달 */}
      <BookDetailModal
        book={selectedBook!}
        isOpen={selectedBook !== null}
        onClose={() => setSelectedBook(null)}
      />
    </div>
  );
}

export default App;

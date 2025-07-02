import React from "react";
import { Sparkles, X } from "lucide-react";
import type { WebNovel } from "@/types";
import { PLATFORMS } from "@/utils/constants";
import { MagicalStars } from "../atoms/MagicalStars";

interface BookDetailModalProps {
  book: WebNovel | null;
  isOpen: boolean;
  onClose: () => void;
}

export const BookDetailModal: React.FC<BookDetailModalProps> = ({
  book,
  isOpen,
  onClose,
}) => {
  if (!isOpen || !book) return null;

  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Escape") {
      onClose();
    }
  };

  return (
    <div
      className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4"
      onClick={handleBackdropClick}
      onKeyDown={handleKeyDown}
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      tabIndex={-1}
    >
      <div className="bg-white/90 backdrop-blur-md rounded-2xl p-6 max-w-md w-full border-2 border-purple-200 shadow-2xl relative overflow-hidden">
        {/* 모달 내부 마법적 별 효과 */}
        <MagicalStars count={8} className="opacity-30" />

        {/* 닫기 버튼 */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-purple-600 hover:text-purple-800 text-2xl font-bold z-20 w-8 h-8 flex items-center justify-center rounded-full hover:bg-purple-100 transition-colors"
          aria-label="모달 닫기"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="relative z-10">
          {/* 책 표지 */}
          <div className="text-center mb-6">
            <img
              src={book.cover}
              alt={`${book.title} 표지`}
              className="w-32 h-40 object-cover rounded-lg mx-auto shadow-lg border-2 border-purple-100"
            />
          </div>

          {/* 책 정보 */}
          <div className="text-center mb-6">
            <h2
              id="modal-title"
              className="text-xl font-bold text-purple-800 mb-2"
            >
              {book.title}
            </h2>
            <p className="text-purple-600 mb-4">by {book.author}</p>

            {/* 별점 */}
            <div className="flex items-center justify-center gap-1 mb-4">
              {[...Array(5)].map((_, i) => (
                <div
                  key={i}
                  className={`w-4 h-4 rounded-full ${
                    i < Math.floor(book.rating)
                      ? "bg-yellow-400"
                      : "bg-gray-300"
                  }`}
                />
              ))}
              <span className="text-yellow-600 ml-2 font-medium">
                ({book.rating})
              </span>
            </div>
          </div>

          {/* AI 추천 이유 */}
          <div className="bg-purple-50/80 rounded-lg p-4 mb-6 border border-purple-100">
            <h3 className="text-purple-700 font-semibold mb-2 flex items-center gap-2">
              <Sparkles className="w-4 h-4" />
              AI의 추천 이유
            </h3>
            <p className="text-purple-600 text-sm">{book.aiReason}</p>
          </div>

          {/* 장르 태그 */}
          <div className="flex flex-wrap gap-2 justify-center mb-6">
            {book.genre.map((genre, i) => (
              <span
                key={i}
                className="bg-purple-100 text-purple-700 text-xs px-3 py-1 rounded-full font-medium"
              >
                {genre}
              </span>
            ))}
          </div>

          {/* 플랫폼 버튼 */}
          <div className="text-center">
            <button
              className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-8 py-3 rounded-full font-bold hover:shadow-lg hover:shadow-purple-300/50 transition-all transform hover:scale-105 flex items-center gap-2 mx-auto"
              onClick={() => {
                window.open(
                  PLATFORMS[book.platform].url,
                  "_blank",
                  "noopener,noreferrer"
                );
              }}
            >
              {PLATFORMS[book.platform].name}에서 읽기
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BookDetailModal;

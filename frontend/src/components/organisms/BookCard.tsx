import React, { useState } from "react";
import { Star } from "lucide-react";
import type { WebNovel } from "@/types";
import { PLATFORMS } from "@/utils/constants";

interface BookCardProps {
  book: WebNovel;
  onClick: (book: WebNovel) => void;
}

export const BookCard: React.FC<BookCardProps> = ({ book, onClick }) => {
  const [logoError, setLogoError] = useState(false);
  return (
    <div
      className="relative group cursor-pointer transition-all duration-300 hover:transform hover:scale-105 hover:shadow-xl hover:shadow-purple-200/50 rounded-xl overflow-hidden aspect-[2/3]"
      onClick={() => onClick(book)}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => (e.key === "Enter" || e.key === " ") && onClick(book)}
      aria-label={`${book.title} - ${book.author} 작품 상세보기`}
    >
      {/* 배경 이미지 */}
      <img
        src={book.cover}
        alt={`${book.title} 표지`}
        className="absolute inset-0 w-full h-full object-cover"
        loading="lazy"
      />

      {/* 그라디언트 오버레이 */}
      <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent" />

      {/* 호버 시 추가 오버레이 */}
      <div className="absolute inset-0 bg-purple-600/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

      {/* 플랫폼 로고 배지 */}
      <div className="absolute top-2 left-2 w-6 h-6 z-10">
        {!logoError ? (
          <img
            src={PLATFORMS[book.platform].logo}
            alt={PLATFORMS[book.platform].name}
            className="w-full h-full object-contain drop-shadow-md rounded-sm"
            title={PLATFORMS[book.platform].name}
            onError={() => setLogoError(true)}
          />
        ) : (
          <div
            className="w-full h-full rounded-sm border-2 border-white shadow-md"
            style={{ backgroundColor: PLATFORMS[book.platform].color }}
            title={PLATFORMS[book.platform].name}
          />
        )}
      </div>

      {/* 컨텐츠 오버레이 */}
      <div className="absolute inset-0 p-4 flex flex-col justify-end z-10">
        {/* 장르 태그 */}
        <div className="flex flex-wrap gap-1 mb-2">
          {book.genre.slice(0, 2).map((genre, i) => (
            <span
              key={i}
              className="bg-white/20 backdrop-blur-sm text-white text-xs px-2 py-1 rounded-full font-medium border border-white/30"
            >
              {genre}
            </span>
          ))}
        </div>

        {/* 제목과 저자 */}
        <h3 className="text-white font-bold text-base mb-1 line-clamp-2 drop-shadow-lg">
          {book.title}
        </h3>
        <p className="text-white/90 text-sm mb-2 drop-shadow-md">
          {book.author}
        </p>

        {/* 별점 */}
        <div
          className="flex items-center gap-1"
          role="img"
          aria-label={`평점 ${book.rating}점`}
        >
          {[...Array(5)].map((_, i) => (
            <Star
              key={i}
              className={`w-3 h-3 drop-shadow-sm ${
                i < Math.floor(book.rating)
                  ? "text-yellow-400 fill-current"
                  : "text-white/40"
              }`}
            />
          ))}
          <span className="text-yellow-400 text-xs ml-1 font-medium drop-shadow-sm">
            ({book.rating})
          </span>
        </div>
      </div>
    </div>
  );
};

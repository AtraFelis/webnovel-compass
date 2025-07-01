import React, { useState } from "react";
import { Search, Sparkles } from "lucide-react";

interface SearchBarProps {
  onSearch?: (query: string) => void;
  placeholder?: string;
}

export const SearchBar: React.FC<SearchBarProps> = ({
  onSearch,
  placeholder = "어떤 이야기를 찾으시나요?",
}) => {
  const [query, setQuery] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch?.(query);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(e.target.value);
  };

  return (
    <div className="py-6">
      <div className="max-w-4xl mx-auto px-6">
        <form onSubmit={handleSubmit} className="relative">
          <div className="relative">
            {/* 검색 아이콘 */}
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-purple-400 w-5 h-5" />

            {/* 검색 입력창 */}
            <input
              type="text"
              value={query}
              onChange={handleInputChange}
              placeholder={placeholder}
              className="w-full pl-12 pr-16 py-4 bg-white rounded-full border-2 border-purple-200 focus:border-purple-400 focus:outline-none transition-all duration-300 text-gray-700 placeholder-purple-400 shadow-sm"
            />

            {/* AI 마법 아이콘 */}
            <button
              type="submit"
              className="absolute right-3 top-1/2 transform -translate-y-1/2 p-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl hover:shadow-lg hover:shadow-purple-300/50 transition-all duration-300 hover:scale-105"
              aria-label="AI 검색"
            >
              <Sparkles className="w-5 h-5" />
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SearchBar;

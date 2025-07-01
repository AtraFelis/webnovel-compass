import React from "react";
import { Compass, User } from "lucide-react";

export const Header: React.FC = () => {
  return (
    <header className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-purple-100 px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        {/* 왼쪽 로고 */}
        <div className="flex items-center gap-3">
          <div className="relative">
            <Compass className="w-8 h-8 text-purple-600 animate-pulse" />
            <div className="absolute inset-0 w-8 h-8 border border-purple-300 rounded-full animate-ping" />
          </div>
          <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
            웹소설나침반
          </h1>
        </div>

        {/* 오른쪽 사용자 프로필 */}
        <div className="flex items-center">
          <button
            className="p-2 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 text-white hover:shadow-lg hover:shadow-purple-300/50 transition-all duration-300 hover:scale-105"
            aria-label="사용자 프로필"
          >
            <User className="w-5 h-5" />
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;

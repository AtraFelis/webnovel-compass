import React from "react";
import { Compass } from "lucide-react";
import { DesktopNavigation } from "./Navigation";
import { ProfileDropdown } from "../molecules/ProfileDropdown";
import { useAppContext } from "@/contexts/AppContext";

export const Header: React.FC = () => {
  const { setCurrentPage } = useAppContext();

  const handleLogoClick = () => {
    setCurrentPage("home");
    // 페이지 최상단으로 스크롤
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <header className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-purple-100 px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        {/* 왼쪽 로고 (클릭 가능) */}
        <button
          onClick={handleLogoClick}
          className="flex items-center gap-3 hover:opacity-80 transition-opacity cursor-pointer group"
          aria-label="홈으로 이동"
        >
          <div className="relative">
            <Compass className="w-8 h-8 text-purple-600 animate-pulse group-hover:animate-spin" />
            <div className="absolute inset-0 w-8 h-8 border border-purple-300 rounded-full animate-ping" />
          </div>
          <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
            웹소설나침반
          </h1>
        </button>

        {/* 중앙 데스크톱 네비게이션 */}
        <DesktopNavigation />

        {/* 오른쪽 프로필 드롭다운 */}
        <ProfileDropdown />
      </div>
    </header>
  );
};

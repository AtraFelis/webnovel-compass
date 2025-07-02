import React from 'react';
import { User, Settings, BookOpen, Heart, LogOut, Sparkles } from 'lucide-react';
import { useDropdown } from '@/hooks/useDropdown';

// 드롭다운 메뉴 아이템 타입
interface DropdownItem {
  icon: React.ComponentType<{ className?: string }>;
  label: string;
  onClick: () => void;
  className?: string;
}

export const ProfileDropdown: React.FC = () => {
  const { isOpen, toggleDropdown, dropdownRef } = useDropdown();

  // 메뉴 아이템들
  const menuItems: DropdownItem[] = [
    {
      icon: User,
      label: '내 프로필',
      onClick: () => console.log('내 프로필 클릭'),
    },
    {
      icon: Heart,
      label: '즐겨찾기',
      onClick: () => console.log('즐겨찾기 클릭'),
    },
    {
      icon: BookOpen,
      label: '읽은 책',
      onClick: () => console.log('읽은 책 클릭'),
    },
    {
      icon: Settings,
      label: '설정',
      onClick: () => console.log('설정 클릭'),
    },
    {
      icon: LogOut,
      label: '로그아웃',
      onClick: () => console.log('로그아웃 클릭'),
      className: 'text-red-600 hover:bg-red-50',
    },
  ];

  return (
    <div className="relative" ref={dropdownRef}>
      {/* 프로필 버튼 */}
      <button
        onClick={toggleDropdown}
        className={`p-2 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 text-white hover:shadow-lg hover:shadow-purple-300/50 transition-all duration-300 hover:scale-105 ${
          isOpen ? 'scale-105 shadow-lg shadow-purple-300/50' : ''
        }`}
        aria-label="사용자 프로필 메뉴"
        aria-expanded={isOpen}
      >
        <User className="w-5 h-5" />
      </button>

      {/* 드롭다운 모달 */}
      {isOpen && (
        <div className="absolute right-0 top-full mt-2 w-56 bg-white/95 backdrop-blur-md rounded-xl border-2 border-purple-200 shadow-xl shadow-purple-200/20 z-50 overflow-hidden">
          {/* 헤더 */}
          <div className="px-4 py-3 bg-gradient-to-r from-purple-50 to-pink-50 border-b border-purple-100">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                <User className="w-5 h-5 text-white" />
              </div>
              <div>
                <p className="font-semibold text-purple-800">사용자님</p>
                <p className="text-xs text-purple-600 flex items-center gap-1">
                  <Sparkles className="w-3 h-3" />
                  AI 추천 전문가
                </p>
              </div>
            </div>
          </div>

          {/* 메뉴 아이템들 */}
          <div className="py-2">
            {menuItems.map((item, index) => {
              const Icon = item.icon;
              return (
                <button
                  key={index}
                  onClick={() => {
                    item.onClick();
                    // 클릭 후 드롭다운 닫기 (로그아웃 제외)
                    if (item.label !== '로그아웃') {
                      // closeDropdown(); // 필요시 주석 해제
                    }
                  }}
                  className={`w-full px-4 py-3 flex items-center gap-3 hover:bg-purple-50 transition-colors text-left ${
                    item.className || 'text-purple-700'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span className="font-medium">{item.label}</span>
                </button>
              );
            })}
          </div>

          {/* 푸터 */}
          <div className="px-4 py-3 bg-gradient-to-r from-purple-50 to-pink-50 border-t border-purple-100">
            <p className="text-xs text-purple-500 text-center">
              웹소설나침반 v1.0.0
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProfileDropdown;

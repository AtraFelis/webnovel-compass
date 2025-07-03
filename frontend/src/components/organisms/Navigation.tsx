import React from 'react';
import { Home, BookOpen, Search } from 'lucide-react';
import { useAppContext } from '@/contexts/AppContext';

// 네비게이션 아이템 타입
interface NavItem {
  icon: React.ComponentType<{ className?: string }>;
  label: string;
  id: string;
}

// 네비게이션 아이템 정의 (Profile 제외)
const NAV_ITEMS: NavItem[] = [
  { icon: Home, label: 'Home', id: 'home' },
  { icon: BookOpen, label: 'Library', id: 'library' },
  { icon: Search, label: 'Search', id: 'search' }
];

// 모바일 하단 네비게이션
export const MobileNavigation: React.FC = () => {
  const { currentPage, setCurrentPage } = useAppContext();

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-white/90 backdrop-blur-md border-t-2 border-purple-200 shadow-lg md:hidden z-50">
      <div className="flex">
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          const isActive = currentPage === item.id;
          
          return (
            <button
              key={item.id}
              onClick={() => setCurrentPage(item.id)}
              className={`flex-1 py-3 px-2 flex flex-col items-center gap-1 transition-all ${
                isActive 
                  ? 'text-purple-600' 
                  : 'text-purple-400 hover:text-purple-500'
              }`}
              aria-label={`${item.label} 페이지로 이동`}
            >
              <Icon className="w-5 h-5" />
              <span className="text-xs font-medium">{item.label}</span>
              {isActive && (
                <div className="w-2 h-2 bg-purple-600 rounded-full" />
              )}
            </button>
          );
        })}
      </div>
    </nav>
  );
};

// 데스크톱 상단 네비게이션
export const DesktopNavigation: React.FC = () => {
  const { currentPage, setCurrentPage } = useAppContext();

  return (
    <nav className="hidden md:flex items-center gap-8">
      {NAV_ITEMS.map((item) => {
        const Icon = item.icon;
        const isActive = currentPage === item.id;
        
        return (
          <button
            key={item.id}
            onClick={() => setCurrentPage(item.id)}
            className={`flex items-center gap-2 px-4 py-2 rounded-full transition-all ${
              isActive 
                ? 'bg-purple-100 text-purple-700' 
                : 'text-purple-500 hover:text-purple-700 hover:bg-purple-50'
            }`}
            aria-label={`${item.label} 페이지로 이동`}
          >
            <Icon className="w-5 h-5" />
            <span className="font-medium">{item.label}</span>
          </button>
        );
      })}
    </nav>
  );
};

export default { MobileNavigation, DesktopNavigation };

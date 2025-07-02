import React from 'react';
import { Sparkles } from 'lucide-react';
import { MagicalStars } from '../atoms/MagicalStars';

interface HeroSectionProps {
  onExploreClick?: () => void;
  className?: string;
}

export const HeroSection: React.FC<HeroSectionProps> = ({ 
  onExploreClick,
  className = '' 
}) => {
  const handleExploreClick = () => {
    if (onExploreClick) {
      onExploreClick();
    } else {
      // 기본 동작: 검색바로 스크롤
      const searchSection = document.querySelector('[data-search-section]');
      searchSection?.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div className={`px-6 mb-6 ${className}`}>
      <div className="max-w-5xl mx-auto">
        <div className="relative bg-gradient-to-r from-purple-200/60 to-pink-200/60 rounded-2xl p-6 lg:p-8 border-2 border-purple-200 backdrop-blur-sm overflow-hidden shadow-lg">
          {/* 배경 마법 별 효과 */}
          <div className="absolute inset-0">
            <MagicalStars count={12} className="opacity-40" />
          </div>
          
          {/* 콘텐츠 */}
          <div className="relative z-10 text-center">
            <h2 className="text-xl lg:text-3xl xl:text-4xl font-bold bg-gradient-to-r from-purple-700 to-pink-700 bg-clip-text text-transparent mb-2 lg:mb-3">
              당신을 위한 맞춤 추천
            </h2>
            <p className="text-purple-600 mb-4 lg:mb-6 font-medium text-sm lg:text-base xl:text-lg">
              AI가 선별한 개인화 웹소설
            </p>
            
            {/* 탐색 시작하기 버튼 */}
            <button 
              onClick={handleExploreClick}
              className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-6 py-2 lg:px-7 lg:py-3 rounded-full font-bold hover:shadow-lg hover:shadow-purple-300/50 transition-all transform hover:scale-105 text-sm lg:text-base flex items-center gap-2 mx-auto group"
            >
              <Sparkles className="w-4 h-4 lg:w-5 lg:h-5 group-hover:rotate-12 transition-transform" />
              탐색 시작하기
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HeroSection;

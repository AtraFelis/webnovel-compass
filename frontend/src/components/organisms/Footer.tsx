import React from 'react';
import { Compass, Heart, Github, Mail, Coffee } from 'lucide-react';

export const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gradient-to-r from-purple-900 via-purple-800 to-pink-800 text-white mt-16">
      <div className="max-w-6xl mx-auto px-6 py-12">
        {/* 메인 푸터 콘텐츠 */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          
          {/* 브랜드 섹션 */}
          <div className="lg:col-span-2">
            <div className="flex items-center gap-3 mb-4">
              <div className="relative">
                <Compass className="w-8 h-8 text-purple-200 animate-pulse" />
                <div className="absolute inset-0 w-8 h-8 border border-purple-300/50 rounded-full animate-ping" />
              </div>
              <h3 className="text-2xl font-bold bg-gradient-to-r from-purple-200 to-pink-200 bg-clip-text text-transparent">
                웹소설나침반
              </h3>
            </div>
            <p className="text-purple-200 mb-4 leading-relaxed">
              AI가 추천하는 개인 맞춤형 웹소설 발견 플랫폼입니다. 
              당신의 취향을 분석하여 완벽한 이야기를 찾아드립니다.
            </p>
            <div className="flex items-center gap-2 text-purple-300">
              <Heart className="w-4 h-4" />
              <span className="text-sm">당신의 다음 이야기를 찾아주는</span>
            </div>
          </div>

          {/* 빠른 링크 */}
          <div>
            <h4 className="text-lg font-semibold mb-4 text-purple-200">빠른 링크</h4>
            <ul className="space-y-2">
              {[
                { label: '홈', href: '#' },
                { label: '도서 검색', href: '#' },
                { label: '인기 작품', href: '#' },
                { label: '신작 소설', href: '#' },
                { label: '장르별', href: '#' },
              ].map((link, index) => (
                <li key={index}>
                  <a 
                    href={link.href}
                    className="text-purple-300 hover:text-white transition-colors text-sm hover:underline"
                  >
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* 지원 및 정보 */}
          <div>
            <h4 className="text-lg font-semibold mb-4 text-purple-200">지원 및 정보</h4>
            <ul className="space-y-2">
              {[
                { label: '이용 가이드', href: '#' },
                { label: '개인정보처리방침', href: '#' },
                { label: '서비스 약관', href: '#' },
                { label: '고객 지원', href: '#' },
                { label: 'FAQ', href: '#' },
              ].map((link, index) => (
                <li key={index}>
                  <a 
                    href={link.href}
                    className="text-purple-300 hover:text-white transition-colors text-sm hover:underline"
                  >
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* 구분선 */}
        <div className="border-t border-purple-600/30 my-8"></div>

        {/* 하단 정보 */}
        <div className="flex flex-col md:flex-row justify-between items-center gap-4">
          
          {/* 저작권 정보 */}
          <div className="text-center md:text-left">
            <p className="text-purple-300 text-sm">
              © {currentYear} 웹소설나침반. All rights reserved.
            </p>
            <p className="text-purple-400 text-xs mt-1">
              AI 기반 개인화 추천 시스템으로 구동됩니다
            </p>
          </div>

          {/* 소셜 링크 및 추가 정보 */}
          <div className="flex items-center gap-6">
            
            {/* 소셜 아이콘들 */}
            <div className="flex items-center gap-3">
              <a 
                href="#" 
                className="p-2 bg-purple-700/50 rounded-full hover:bg-purple-600/50 transition-colors"
                aria-label="GitHub"
              >
                <Github className="w-4 h-4 text-purple-200" />
              </a>
              <a 
                href="#" 
                className="p-2 bg-purple-700/50 rounded-full hover:bg-purple-600/50 transition-colors"
                aria-label="이메일 문의"
              >
                <Mail className="w-4 h-4 text-purple-200" />
              </a>
              <a 
                href="#" 
                className="p-2 bg-purple-700/50 rounded-full hover:bg-purple-600/50 transition-colors"
                aria-label="후원하기"
              >
                <Coffee className="w-4 h-4 text-purple-200" />
              </a>
            </div>

            {/* 버전 정보 */}
            <div className="text-purple-400 text-xs">
              v1.0.0
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

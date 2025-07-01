import React, { useMemo } from 'react';

interface MagicalStarsProps {
  count?: number;
  className?: string;
}

interface StarProps {
  left: string;
  top: string;
  size: string;
  animationDelay: string;
  animationDuration: string;
}

export const MagicalStars: React.FC<MagicalStarsProps> = ({ 
  count = 20, 
  className = '' 
}) => {
  // 별들의 속성을 미리 계산하여 성능 최적화
  const stars = useMemo(() => {
    return Array.from({ length: count }, (_, i) => ({
      id: i,
      left: `${Math.random() * 100}%`,
      top: `${Math.random() * 100}%`,
      size: ['w-1 h-1', 'w-2 h-2', 'w-1.5 h-1.5'][Math.floor(Math.random() * 3)],
      animationDelay: `${Math.random() * 2}s`,
      animationDuration: `${2 + Math.random() * 2}s`
    } as StarProps & { id: number }));
  }, [count]);

  return (
    <div className={`absolute inset-0 overflow-hidden pointer-events-none ${className}`}>
      {stars.map((star) => (
        <div
          key={star.id}
          className={`absolute ${star.size} bg-gradient-to-r from-yellow-400 to-pink-400 rounded-full animate-pulse shadow-lg`}
          style={{
            left: star.left,
            top: star.top,
            animationDelay: star.animationDelay,
            animationDuration: star.animationDuration
          }}
        />
      ))}
    </div>
  );
};

export default MagicalStars;

import { useState, useRef, useEffect } from 'react';

/**
 * 드롭다운 모달 상태와 액션을 관리하는 커스텀 훅
 */
export const useDropdown = () => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // 드롭다운 토글
  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  // 드롭다운 닫기
  const closeDropdown = () => {
    setIsOpen(false);
  };

  // 외부 클릭 시 드롭다운 닫기
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        closeDropdown();
      }
    };

    // ESC 키로 닫기
    const handleEscapeKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        closeDropdown();
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      document.addEventListener('keydown', handleEscapeKey);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleEscapeKey);
    };
  }, [isOpen]);

  return {
    isOpen,
    toggleDropdown,
    closeDropdown,
    dropdownRef,
  };
};

export default useDropdown;

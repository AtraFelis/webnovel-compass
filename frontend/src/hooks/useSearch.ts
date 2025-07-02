import { useAppContext } from '@/contexts/AppContext';

/**
 * 검색 관련 상태와 액션을 관리하는 커스텀 훅
 */
export const useSearch = () => {
  const {
    searchQuery,
    filteredBooks,
    isLoading,
    setSearchQuery,
    handleSearch,
  } = useAppContext();

  // 검색 결과 통계
  const searchStats = {
    total: filteredBooks.length,
    hasResults: filteredBooks.length > 0,
    isSearching: searchQuery.trim() !== '',
    isEmpty: filteredBooks.length === 0 && searchQuery.trim() !== '',
  };

  return {
    // 상태
    searchQuery,
    filteredBooks,
    isLoading,
    searchStats,
    
    // 액션
    setSearchQuery,
    handleSearch,
    
    // 편의 함수
    clearSearch: () => handleSearch(''),
    isSearchActive: searchQuery.trim() !== '',
  };
};

export default useSearch;

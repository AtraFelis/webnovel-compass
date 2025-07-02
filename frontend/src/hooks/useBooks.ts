import { useAppContext } from '@/contexts/AppContext';
import type { WebNovel } from '@/types';

/**
 * 책 관련 상태와 액션을 관리하는 커스텀 훅
 */
export const useBooks = () => {
  const {
    books,
    filteredBooks,
    selectedBook,
    isLoading,
    setSelectedBook,
    selectBook,
  } = useAppContext();

  return {
    // 상태
    books,
    filteredBooks,
    selectedBook,
    isLoading,
    
    // 액션
    setSelectedBook,
    selectBook,
    
    // 계산된 값
    hasBooks: books.length > 0,
    hasFilteredBooks: filteredBooks.length > 0,
    selectedBookId: selectedBook?.id || null,
  };
};

export default useBooks;

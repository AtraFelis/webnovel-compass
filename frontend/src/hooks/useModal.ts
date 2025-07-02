import { useAppContext } from '@/contexts/AppContext';
import type { WebNovel } from '@/types';

/**
 * 모달 상태와 액션을 관리하는 커스텀 훅
 */
export const useModal = () => {
  const {
    selectedBook,
    setSelectedBook,
    selectBook,
  } = useAppContext();

  // 모달 상태
  const isOpen = selectedBook !== null;

  // 모달 열기
  const openModal = (book: WebNovel) => {
    selectBook(book);
  };

  // 모달 닫기
  const closeModal = () => {
    setSelectedBook(null);
  };

  // 모달 토글
  const toggleModal = (book?: WebNovel) => {
    if (isOpen) {
      closeModal();
    } else if (book) {
      openModal(book);
    }
  };

  return {
    // 상태
    isOpen,
    selectedBook,
    
    // 액션
    openModal,
    closeModal,
    toggleModal,
    
    // 편의 프로퍼티
    modalData: selectedBook,
  };
};

export default useModal;

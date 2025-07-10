"""
유사도 계산 유틸리티
"""
from typing import List, Set
from app.schemas import Novel


class SimilarityCalculator:
    """웹소설 간 유사도 계산 유틸리티"""
    
    @staticmethod
    def calculate_novel_similarity(
        base_novel: Novel, 
        target_novel: Novel
    ) -> float:
        """두 웹소설 간 유사도 계산"""
        if base_novel.id == target_novel.id:
            return 0.0  # 자기 자신과는 유사도 0
        
        similarity_score = 0.0
        
        # 1. 장르 유사도 (가중치 0.5)
        if base_novel.genre == target_novel.genre:
            similarity_score += 0.5
        
        # 2. 태그 유사도 (가중치 0.3)
        tag_similarity = SimilarityCalculator._calculate_tag_similarity(
            base_novel.tags, target_novel.tags
        )
        similarity_score += tag_similarity * 0.3
        
        # 3. 평점 유사도 (가중치 0.2)
        rating_similarity = SimilarityCalculator._calculate_rating_similarity(
            base_novel.average_rating, target_novel.average_rating
        )
        similarity_score += rating_similarity * 0.2
        
        return similarity_score
    
    @staticmethod
    def _calculate_tag_similarity(tags1: List[str], tags2: List[str]) -> float:
        """태그 유사도 계산 (Jaccard 유사도)"""
        if not tags1 or not tags2:
            return 0.0
        
        set1 = set(tags1)
        set2 = set(tags2)
        
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        return intersection / union if union > 0 else 0.0
    
    @staticmethod
    def _calculate_rating_similarity(rating1: float, rating2: float) -> float:
        """평점 유사도 계산"""
        if rating1 is None or rating2 is None:
            return 0.0
        
        # 평점 차이를 유사도로 변환 (차이가 적을수록 높은 유사도)
        rating_diff = abs(rating1 - rating2)
        return max(0, 1 - rating_diff / 5.0)
    
    @staticmethod
    def find_similar_novels(
        base_novel: Novel,
        candidate_novels: List[Novel],
        similarity_threshold: float = 0.1,
        limit: int = 10
    ) -> List[tuple[Novel, float]]:
        """유사한 웹소설 찾기"""
        similar_novels = []
        
        for novel in candidate_novels:
            similarity = SimilarityCalculator.calculate_novel_similarity(
                base_novel, novel
            )
            
            if similarity >= similarity_threshold:
                similar_novels.append((novel, similarity))
        
        # 유사도 순으로 정렬
        similar_novels.sort(key=lambda x: x[1], reverse=True)
        
        return similar_novels[:limit]

package com.webnovelcompass.user.repository;

import com.webnovelcompass.user.entity.UserPreferredAuthor;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface UserPreferredAuthorRepository extends JpaRepository<UserPreferredAuthor, Long> {
    List<UserPreferredAuthor> findByUserId(Long userId);
    Optional<UserPreferredAuthor> findByUserIdAndAuthorId(Long userId, String authorId);
    void deleteByUserIdAndAuthorId(Long userId, String authorId);
}
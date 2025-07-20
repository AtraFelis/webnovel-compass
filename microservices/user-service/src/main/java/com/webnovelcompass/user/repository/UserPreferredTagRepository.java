package com.webnovelcompass.user.repository;

import com.webnovelcompass.user.entity.UserPreferredTag;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface UserPreferredTagRepository extends JpaRepository<UserPreferredTag, Long> {
    List<UserPreferredTag> findByUserId(Long userId);
    Optional<UserPreferredTag> findByUserIdAndTagId(Long userId, Long tagId);
    void deleteByUserIdAndTagId(Long userId, Long tagId);
}
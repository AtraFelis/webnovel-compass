package com.webnovelcompass.user.repository;

import com.webnovelcompass.user.entity.UserPreferredGenre;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface UserPreferredGenreRepository extends JpaRepository<UserPreferredGenre, Long> {
    List<UserPreferredGenre> findByUserId(Long userId);
    Optional<UserPreferredGenre> findByUserIdAndGenreId(Long userId, Long genreId);
    void deleteByUserIdAndGenreId(Long userId, Long genreId);
}
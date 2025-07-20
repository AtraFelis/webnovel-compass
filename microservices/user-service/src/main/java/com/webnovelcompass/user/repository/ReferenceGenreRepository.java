package com.webnovelcompass.user.repository;

import com.webnovelcompass.user.entity.reference.ReferenceGenre;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface ReferenceGenreRepository extends JpaRepository<ReferenceGenre, Long> {
    Optional<ReferenceGenre> findByGenreId(Long genreId);
    boolean existsByGenreId(Long genreId);
}
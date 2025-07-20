package com.webnovelcompass.user.repository;

import com.webnovelcompass.user.entity.reference.ReferenceAuthor;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface ReferenceAuthorRepository extends JpaRepository<ReferenceAuthor, String> {
    Optional<ReferenceAuthor> findByAuthorId(String authorId);
    boolean existsByAuthorId(String authorId);
}
package com.webnovelcompass.user.repository;

import com.webnovelcompass.user.entity.reference.ReferenceTag;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface ReferenceTagRepository extends JpaRepository<ReferenceTag, Long> {
    Optional<ReferenceTag> findByTagId(Long tagId);
    boolean existsByTagId(Long tagId);
}
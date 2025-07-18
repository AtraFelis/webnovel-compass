package com.webnovelcompass.user.entity.reference;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Getter;

import java.time.LocalDateTime;

@Entity
@Table(name = "reference_authors")
@Getter
public class ReferenceAuthor {

    @Id
    private String authorId;           // Content Service와 동일한 ID (VARCHAR(36))

    @Column(nullable = false, length = 100)
    private String name;            // 사용자에게 표시할 이름

    @Column(name = "last_synced_at")
    private LocalDateTime lastSyncedAt;  // 동기화 추적
}
package com.webnovelcompass.user.entity.reference;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Getter;

import java.time.LocalDateTime;

@Entity
@Table(name = "reference_genres")
@Getter
public class ReferenceGenre {
    @Id
    private Long genreId;           // Content Service와 동일한 ID

    @Column(nullable = false, length = 50)
    private String name;            // 사용자에게 표시할 이름

    @Column(name = "last_synced_at")
    private LocalDateTime lastSyncedAt;  // 동기화 추적
}
package com.webnovelcompass.user.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.time.LocalDateTime;

@EntityListeners(AuditingEntityListener.class)
@Entity
@Table(name = "user_social_accounts")
@NoArgsConstructor
@Getter
public class UserSocialAccounts {
    
    @Id
    @Column(name = "social_account_id")
    private Long socialAccountId;

    @OneToOne
    @JoinColumn(name = "user_id", nullable = false)
    private User user;
    
    @Enumerated(EnumType.STRING)
    @Column(name = "provider", nullable = false)
    private Provider provider;
    
    @Column(name = "provider_id", nullable = false, length = 255)
    private String providerId;
    
    @Column(name = "provider_email", length = 255)
    private String providerEmail;
    
    @Column(name = "is_primary")
    private Boolean isPrimary;

    @CreatedDate
    @Column(name = "connected_at")
    private LocalDateTime connectedAt;
    
    @Column(name = "last_used_at")
    private LocalDateTime lastUsedAt;
    
    public enum Provider {
        GOOGLE, NAVER, KAKAO
    }
}
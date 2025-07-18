package com.webnovelcompass.user.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.time.LocalDateTime;

@EntityListeners(AuditingEntityListener.class)
@Entity
@NoArgsConstructor
@Table(name = "user_consents")
@Getter
public class UserConsents {
    
    @Id
    @Column(name = "consent_id")
    private Long consentId;
    
    @Column(name = "user_id", nullable = false)
    private Long userId;
    
    @Column(name = "terms_of_service")
    private Boolean termsOfService;
    
    @Column(name = "privacy_policy")
    private Boolean privacyPolicy;
    
    @Column(name = "marketing_email")
    private Boolean marketingEmail;
    
    @Column(name = "marketing_sms")
    private Boolean marketingSms;
    
    @Column(name = "marketing_push")
    private Boolean marketingPush;
    
    @Column(name = "personalization")
    private Boolean personalization;
    
    @Column(name = "behavior_tracking")
    private Boolean behaviorTracking;
    
    @Column(name = "cookies")
    private Boolean cookies;

    @CreatedDate
    @Column(name = "consented_at")
    private LocalDateTime consentedAt;

    @LastModifiedDate
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
}

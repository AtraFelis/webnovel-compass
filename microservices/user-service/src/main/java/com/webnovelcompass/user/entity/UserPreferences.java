package com.webnovelcompass.user.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

import java.math.BigDecimal;

@Entity
@Table(name = "user_preferences")
@RequiredArgsConstructor
@Getter
public class UserPreferences extends BaseTimeEntity{
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToOne
    @JoinColumn(name = "user_id")
    private User user;
    
    @Column(name = "adult_content_filter")
    private Boolean adultContentFilter;
    
    @Enumerated(EnumType.STRING)
    @Column(name = "preferred_length")
    private PreferredLength preferredLength = PreferredLength.ANY;
    
    @Enumerated(EnumType.STRING)
    @Column(name = "preferred_status")
    private PreferredStatus preferredStatus = PreferredStatus.ANY;
    
    @Enumerated(EnumType.STRING)
    @Column(name = "recommendation_sensitivity")
    private RecommendationSensitivity recommendationSensitivity;
    
    @Column(name = "algorithm_weight_collaborative", precision = 3, scale = 2)
    private BigDecimal algorithmWeightCollaborative = new BigDecimal("0.60");
    
    @Column(name = "algorithm_weight_content_based", precision = 3, scale = 2)
    private BigDecimal algorithmWeightContentBased = new BigDecimal("0.40");
    
    @Column(name = "diversity_preference", precision = 3, scale = 2)
    private BigDecimal diversityPreference = new BigDecimal("0.50");
    
    public enum PreferredLength {
        SHORT, MEDIUM, LONG, ANY
    }
    
    public enum PreferredStatus {
        COMPLETED, ONGOING, ANY
    }
    
    public enum RecommendationSensitivity {
        CONSERVATIVE, BALANCED, ADVENTUROUS
    }
}

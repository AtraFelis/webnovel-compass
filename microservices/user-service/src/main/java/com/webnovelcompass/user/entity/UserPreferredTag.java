package com.webnovelcompass.user.entity;

import com.webnovelcompass.user.entity.reference.ReferenceTag;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;

@Entity
@Table(name = "user_preferred_tags")
@NoArgsConstructor
@Getter
public class UserPreferredTag extends BaseTimeEntity {
    
    @Id
    @Column(name = "preference_id")
    private Long preferenceId;

    @OneToOne
    @JoinColumn(name = "user_id")
    private User user;

    @OneToOne
    @JoinColumn(name = "tag_id", nullable = false)
    private ReferenceTag tag;
    
    @Column(name = "preference_score", nullable = false, precision = 3, scale = 2)
    private BigDecimal preferenceScore;
    
    @Column(name = "is_explicit")
    private Boolean isExplicit;
    
    @Column(name = "confidence_level", precision = 3, scale = 2)
    private BigDecimal confidenceLevel;
    
    @Column(name = "interaction_count")
    private Integer interactionCount;
    
    @Column(name = "last_interaction_type", length = 50)
    private String lastInteractionType;
    
    @Column(name = "last_updated_by", length = 20)
    private String lastUpdatedBy = "SYSTEM";
}

package com.webnovelcompass.user.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Entity
@NoArgsConstructor
@Getter
@Table(name = "users")
public class User extends BaseTimeEntity {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "user_id")
    private Long userId;
    
    @Column(name = "username", nullable = false, length = 50)
    private String username;
    
    @Column(name = "email", nullable = false, length = 255)
    private String email;
    
    @Column(name = "password_hash", nullable = false, length = 255)
    private String passwordHash;
    
    @Column(name = "nickname", length = 100)
    private String nickname;
    
    @Enumerated(EnumType.STRING)
    @Column(name = "status")
    private UserStatus status;
    
    @Column(name = "profile_image_url", columnDefinition = "TEXT")
    private String profileImageUrl;
    
    @Column(name = "birth_year")
    private Integer birthYear;
    
    @Column(name = "gender", length = 1)
    private String gender;
    
    @Column(name = "last_login_at")
    private LocalDateTime lastLoginAt;
    
    public enum UserStatus {
        ACTIVE, DORMANT, SUSPENDED, DELETED
    }
}

package com.webnovelcompass.content.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/novels")
public class NovelController {

    @GetMapping("/health")
    public String health() {
        return "Content Service is running! 📚";
    }
}
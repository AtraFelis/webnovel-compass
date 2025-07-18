package com.webnovelcompass.analytics.controller;

import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;

import java.time.LocalDateTime;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/analytics")
public class AnalyticsController {

    @GetMapping("/health")
    public Mono<String> health() {
        return Mono.just("Analytics Service is running! 📊");
    }

    @PostMapping("/events")
    public Mono<Map<String, Object>> collectEvent(@RequestBody Map<String, Object> event) {
        // TODO: 이벤트 수집 로직
        return Mono.just(Map.of(
                "status", "collected",
                "timestamp", LocalDateTime.now()
        ));
    }
}

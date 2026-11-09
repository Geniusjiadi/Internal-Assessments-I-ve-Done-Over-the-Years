from __future__ import annotations


def clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def duration_score(duration_minutes: float, target_minutes: float = 480.0) -> float:
    return clamp(100.0 - abs(duration_minutes - target_minutes) * 0.4)


def latency_score(latency_minutes: float) -> float:
    if latency_minutes <= 20:
        return 100.0
    return clamp(100.0 - (latency_minutes - 20) * 2.0)


def quality_score(quality: float) -> float:
    return clamp((quality / 5.0) * 100.0)


def lifestyle_score(pre_bed_screen_minutes: float | None, late_caffeine_mg: float, exercise_minutes: float) -> float:
    score = 100.0
    if pre_bed_screen_minutes is not None:
        score -= min(50.0, pre_bed_screen_minutes * 0.5)
    score -= min(40.0, late_caffeine_mg * 0.35)
    score += min(10.0, exercise_minutes * 0.2)
    return clamp(score)


def calculate_sleep_score(day: dict, regularity_score: float | None) -> dict:
    regularity = 70.0 if regularity_score is None else regularity_score
    components = {
        "duration": duration_score(day["duration_minutes"]),
        "regularity": clamp(regularity),
        "latency": latency_score(day["latency_minutes"]),
        "quality": quality_score(day["quality"]),
        "lifestyle": lifestyle_score(
            day.get("pre_bed_screen_minutes"),
            day.get("late_caffeine_mg", 0),
            day.get("exercise_minutes", 0),
        ),
    }
    weights = {
        "duration": 0.35,
        "regularity": 0.20,
        "latency": 0.15,
        "quality": 0.20,
        "lifestyle": 0.10,
    }
    total = sum(components[key] * weights[key] for key in components)
    return {
        "score": round(total, 1),
        "components": {k: round(v, 1) for k, v in components.items()},
        "weights": weights,
    }

from __future__ import annotations

from statistics import mean
from .trend_analyzer import rolling_period_comparison, regularity_analysis, weekday_weekend_analysis
from .correlation_engine import spearman_rank_correlation, confidence_from_sample
from .sleep_score import calculate_sleep_score
from .sleep_calculator import minutes_to_hhmm


CORRELATION_DEFINITIONS = [
    ("pre_bed_screen_minutes", "quality", "Pre-bed screen time vs sleep quality"),
    ("late_caffeine_mg", "latency_minutes", "Late caffeine vs sleep latency"),
    ("exercise_minutes", "quality", "Exercise duration vs sleep quality"),
    ("pre_bed_screen_minutes", "duration_minutes", "Pre-bed screen time vs sleep duration"),
]


def analyze_correlations(rows: list[dict]) -> list[dict]:
    results = []
    for x_key, y_key, label in CORRELATION_DEFINITIONS:
        result = spearman_rank_correlation(
            [r.get(x_key) for r in rows],
            [r.get(y_key) for r in rows],
        )
        result.update({
            "x": x_key,
            "y": y_key,
            "label": label,
            "confidence": confidence_from_sample(result["sample_size"]),
        })
        results.append(result)
    return results


def build_analytics(rows: list[dict]) -> dict:
    ordered = sorted(rows, key=lambda r: r["sleep_date"])
    regularity = regularity_analysis(ordered)
    week_compare = weekday_weekend_analysis(ordered)
    trends = {
        "sleep_duration_7d": rolling_period_comparison(ordered, "duration_minutes", 7),
        "sleep_duration_30d": rolling_period_comparison(ordered, "duration_minutes", 30),
        "quality_7d": rolling_period_comparison(ordered, "quality", 7),
        "latency_7d": rolling_period_comparison(ordered, "latency_minutes", 7),
    }
    correlations = analyze_correlations(ordered)

    score = None
    if ordered:
        score = calculate_sleep_score(ordered[-1], regularity.get("regularity_score"))

    return {
        "regularity": regularity,
        "weekday_weekend": week_compare,
        "trends": trends,
        "correlations": correlations,
        "latest_sleep_score": score,
        "record_count": len(ordered),
    }


def trend_series(rows: list[dict], days: int) -> list[dict]:
    chosen = sorted(rows, key=lambda r: r["sleep_date"])[-days:]
    regularity = regularity_analysis(chosen)
    result = []
    for row in chosen:
        score = calculate_sleep_score(row, regularity.get("regularity_score"))
        result.append({
            "date": str(row["sleep_date"]),
            "duration_minutes": row["duration_minutes"],
            "bedtime": row["bedtime"],
            "wake_time": row["wake_time"],
            "quality": row["quality"],
            "latency_minutes": row["latency_minutes"],
            "sleep_score": score["score"],
            "pre_bed_screen_minutes": row.get("pre_bed_screen_minutes"),
            "late_caffeine_mg": row.get("late_caffeine_mg", 0),
        })
    return result

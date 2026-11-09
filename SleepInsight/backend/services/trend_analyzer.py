from __future__ import annotations

from statistics import mean, pstdev
from datetime import datetime
from .sleep_calculator import normalize_bedtime_minutes, clock_minutes, circular_mean_minutes, circular_distance_minutes


def rolling_period_comparison(records: list[dict], field: str, window: int) -> dict:
    values = [r.get(field) for r in sorted(records, key=lambda r: r["sleep_date"]) if r.get(field) is not None]
    if not values:
        return {"current": None, "previous": None, "change": None, "sample_size": 0}
    current_values = values[-window:]
    current = mean(current_values)
    previous = None
    change = None
    if len(values) >= window * 2:
        previous_values = values[-window * 2:-window]
        previous = mean(previous_values)
        change = current - previous
    return {
        "current": round(current, 2),
        "previous": round(previous, 2) if previous is not None else None,
        "change": round(change, 2) if change is not None else None,
        "sample_size": len(current_values),
    }


def regularity_analysis(records: list[dict], lookback: int = 14) -> dict:
    chosen = sorted(records, key=lambda r: r["sleep_date"])[-lookback:]
    if len(chosen) < 2:
        return {"bedtime_sd": None, "wake_time_sd": None, "regularity_score": None, "sample_size": len(chosen)}

    bed_values = [normalize_bedtime_minutes(r["bedtime"]) for r in chosen]
    wake_values = [clock_minutes(r["wake_time"]) for r in chosen]

    bedtime_sd = pstdev(bed_values)
    wake_sd = pstdev(wake_values)
    avg_sd = (bedtime_sd + wake_sd) / 2
    score = max(0.0, min(100.0, 100.0 - avg_sd))

    return {
        "bedtime_sd": round(bedtime_sd, 2),
        "wake_time_sd": round(wake_sd, 2),
        "regularity_score": round(score, 1),
        "sample_size": len(chosen),
    }


def weekday_weekend_analysis(records: list[dict]) -> dict:
    weekday = []
    weekend = []
    for r in records:
        d = r["sleep_date"]
        if isinstance(d, str):
            d = datetime.strptime(d, "%Y-%m-%d").date()
        target = weekend if d.weekday() >= 5 else weekday
        target.append(r)

    def summarize(group: list[dict]) -> dict:
        if not group:
            return {"count": 0}
        bed = circular_mean_minutes([clock_minutes(r["bedtime"]) for r in group])
        wake = circular_mean_minutes([clock_minutes(r["wake_time"]) for r in group])
        midpoint = circular_mean_minutes([r["sleep_midpoint_minutes"] for r in group])
        return {
            "count": len(group),
            "avg_bedtime_minutes": round(bed, 1) if bed is not None else None,
            "avg_wake_minutes": round(wake, 1) if wake is not None else None,
            "avg_duration_minutes": round(mean(r["duration_minutes"] for r in group), 1),
            "avg_quality": round(mean(r["quality"] for r in group), 2),
            "avg_midpoint_minutes": round(midpoint, 1) if midpoint is not None else None,
        }

    wd = summarize(weekday)
    we = summarize(weekend)
    social_jetlag = None
    if wd.get("avg_midpoint_minutes") is not None and we.get("avg_midpoint_minutes") is not None:
        social_jetlag = round(circular_distance_minutes(wd["avg_midpoint_minutes"], we["avg_midpoint_minutes"]), 1)

    return {"weekday": wd, "weekend": we, "social_jetlag_minutes": social_jetlag}

from __future__ import annotations

from datetime import datetime, timedelta
from .sleep_calculator import clock_minutes, circular_distance_minutes


def goal_progress(goal: dict, rows: list[dict]) -> dict:
    start = goal["start_date"]
    if isinstance(start, str):
        start = datetime.strptime(start, "%Y-%m-%d").date()
    end = goal.get("end_date")
    if isinstance(end, str):
        end = datetime.strptime(end, "%Y-%m-%d").date()

    eligible = []
    for row in rows:
        d = row["sleep_date"]
        if isinstance(d, str):
            d = datetime.strptime(d, "%Y-%m-%d").date()
        if d < start or (end and d > end):
            continue
        eligible.append(row)

    eligible = sorted(eligible, key=lambda r: r["sleep_date"])[-7:]
    met = 0
    evaluated = 0

    for row in eligible:
        ok = False
        goal_type = goal["goal_type"]
        if goal_type == "minimum_sleep_minutes":
            evaluated += 1
            ok = row["duration_minutes"] >= float(goal["target_value"])
        elif goal_type == "bedtime_before":
            evaluated += 1
            bed = clock_minutes(row["bedtime"])
            target = clock_minutes(goal["target_time"])
            # Map post-midnight values forward so 00:10 can be compared with 23:30.
            if bed < 12 * 60:
                bed += 1440
            if target < 12 * 60:
                target += 1440
            ok = bed <= target
        elif goal_type == "prebed_screen_max":
            if row.get("pre_bed_screen_minutes") is None:
                continue
            evaluated += 1
            ok = row["pre_bed_screen_minutes"] <= float(goal["target_value"])
        elif goal_type == "max_sleep_latency":
            evaluated += 1
            ok = row["latency_minutes"] <= float(goal["target_value"])
        if ok:
            met += 1

    target_nights = int(goal.get("target_nights_per_week", 5))
    percentage = 0.0 if target_nights == 0 else min(100.0, met / target_nights * 100.0)
    return {
        "met_nights": met,
        "evaluated_nights": evaluated,
        "target_nights": target_nights,
        "completion_percent": round(percentage, 1),
    }


def adaptive_goal_suggestion(goal: dict, progress: dict) -> dict:
    if not goal.get("adaptive_enabled"):
        return {"action": "disabled", "suggested_target": None}

    completion = progress["completion_percent"]
    if completion < 80:
        return {"action": "maintain", "suggested_target": None}

    goal_type = goal["goal_type"]
    if goal_type == "minimum_sleep_minutes":
        return {"action": "increase", "suggested_target": float(goal["target_value"]) + 15}
    if goal_type == "bedtime_before":
        target = clock_minutes(goal["target_time"])
        target = (target - 15) % 1440
        return {"action": "earlier", "suggested_target": f"{target // 60:02d}:{target % 60:02d}"}
    if goal_type in {"prebed_screen_max", "max_sleep_latency"}:
        value = max(0.0, float(goal["target_value"]) - 5)
        return {"action": "decrease", "suggested_target": value}
    return {"action": "maintain", "suggested_target": None}

from __future__ import annotations

from collections import defaultdict
from .sleep_calculator import clock_minutes


def build_daily_features(
    sleep_records: list[dict],
    caffeine_events: list[dict],
    exercise_sessions: list[dict],
    screen_records: list[dict],
) -> list[dict]:
    caffeine_by_date = defaultdict(list)
    exercise_by_date = defaultdict(list)
    screen_by_date = {}

    for item in caffeine_events:
        caffeine_by_date[str(item["event_date"])].append(item)
    for item in exercise_sessions:
        exercise_by_date[str(item["event_date"])].append(item)
    for item in screen_records:
        screen_by_date[str(item["event_date"])] = item

    rows = []
    for sleep in sleep_records:
        key = str(sleep["sleep_date"])
        caffeine = caffeine_by_date.get(key, [])
        exercise = exercise_by_date.get(key, [])
        screen = screen_by_date.get(key)

        late_caffeine = sum(
            float(event["amount_mg"])
            for event in caffeine
            if clock_minutes(event["time"]) >= 14 * 60
        )
        row = dict(sleep)
        row.update({
            "caffeine_total_mg": round(sum(float(e["amount_mg"]) for e in caffeine), 2),
            "late_caffeine_mg": round(late_caffeine, 2),
            "exercise_minutes": sum(int(e["duration_minutes"]) for e in exercise),
            "pre_bed_screen_minutes": screen["pre_bed_minutes"] if screen else None,
            "total_screen_minutes": screen["total_minutes"] if screen else None,
        })
        rows.append(row)
    return rows

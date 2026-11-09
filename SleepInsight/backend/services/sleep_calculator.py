from __future__ import annotations

from datetime import datetime, timedelta, date
import math


def parse_clock(value: str) -> tuple[int, int]:
    try:
        dt = datetime.strptime(value, "%H:%M")
    except ValueError as exc:
        raise ValueError("time must use HH:MM") from exc
    return dt.hour, dt.minute


def clock_minutes(value: str) -> int:
    h, m = parse_clock(value)
    return h * 60 + m


def calculate_sleep_metrics(
    sleep_date: date,
    bedtime: str,
    wake_time: str,
    latency_minutes: int = 0,
) -> dict:
    if latency_minutes < 0:
        raise ValueError("latency_minutes cannot be negative")

    bh, bm = parse_clock(bedtime)
    wh, wm = parse_clock(wake_time)

    bed_dt = datetime.combine(sleep_date, datetime.min.time()).replace(hour=bh, minute=bm)
    wake_dt = datetime.combine(sleep_date, datetime.min.time()).replace(hour=wh, minute=wm)

    if wake_dt <= bed_dt:
        wake_dt += timedelta(days=1)

    actual_start = bed_dt + timedelta(minutes=latency_minutes)
    if wake_dt <= actual_start:
        raise ValueError("wake time must occur after actual sleep start")

    duration = int((wake_dt - actual_start).total_seconds() // 60)
    if duration > 18 * 60:
        raise ValueError("calculated sleep duration exceeds 18 hours")

    midpoint = actual_start + (wake_dt - actual_start) / 2
    midpoint_minutes = midpoint.hour * 60 + midpoint.minute

    return {
        "actual_sleep_start_iso": actual_start.isoformat(timespec="minutes"),
        "duration_minutes": duration,
        "sleep_midpoint_minutes": midpoint_minutes,
    }


def normalize_bedtime_minutes(value: str) -> int:
    """Map post-midnight bedtime values next to late-evening values."""
    minutes = clock_minutes(value)
    return minutes + 1440 if minutes < 12 * 60 else minutes


def circular_mean_minutes(values: list[float]) -> float | None:
    if not values:
        return None
    angles = [2 * math.pi * (v % 1440) / 1440 for v in values]
    x = sum(math.cos(a) for a in angles) / len(angles)
    y = sum(math.sin(a) for a in angles) / len(angles)
    if abs(x) < 1e-12 and abs(y) < 1e-12:
        return None
    angle = math.atan2(y, x)
    if angle < 0:
        angle += 2 * math.pi
    return angle * 1440 / (2 * math.pi)


def circular_distance_minutes(a: float, b: float) -> float:
    diff = abs((a % 1440) - (b % 1440))
    return min(diff, 1440 - diff)


def minutes_to_hhmm(minutes: float | int) -> str:
    minutes = int(round(minutes)) % 1440
    return f"{minutes // 60:02d}:{minutes % 60:02d}"

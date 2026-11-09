from __future__ import annotations

from datetime import datetime, date
from typing import Any

VALID_INTENSITIES = {"Low", "Moderate", "High"}
VALID_GOAL_TYPES = {
    "minimum_sleep_minutes",
    "bedtime_before",
    "prebed_screen_max",
    "max_sleep_latency",
}


def parse_date(value: Any, field: str) -> date:
    if not value:
        raise ValueError(f"{field} is required")
    try:
        return datetime.strptime(str(value), "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError(f"{field} must use YYYY-MM-DD") from exc


def validate_time(value: Any, field: str) -> str:
    if not value:
        raise ValueError(f"{field} is required")
    try:
        parsed = datetime.strptime(str(value), "%H:%M")
    except ValueError as exc:
        raise ValueError(f"{field} must use 24-hour HH:MM format") from exc
    return parsed.strftime("%H:%M")


def non_negative_number(value: Any, field: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be numeric") from exc
    if number < 0:
        raise ValueError(f"{field} cannot be negative")
    return number


def non_negative_int(value: Any, field: str) -> int:
    number = non_negative_number(value, field)
    if not number.is_integer():
        raise ValueError(f"{field} must be a whole number")
    return int(number)


def validate_sleep_payload(data: dict) -> dict:
    cleaned = {
        "sleep_date": parse_date(data.get("sleep_date"), "sleep_date"),
        "bedtime": validate_time(data.get("bedtime"), "bedtime"),
        "wake_time": validate_time(data.get("wake_time"), "wake_time"),
        "latency_minutes": non_negative_int(data.get("latency_minutes", 0), "latency_minutes"),
        "awakenings": non_negative_int(data.get("awakenings", 0), "awakenings"),
        "notes": (data.get("notes") or "").strip() or None,
    }
    try:
        quality = int(data.get("quality"))
    except (TypeError, ValueError) as exc:
        raise ValueError("quality must be an integer from 1 to 5") from exc
    if not 1 <= quality <= 5:
        raise ValueError("quality must be between 1 and 5")
    cleaned["quality"] = quality
    if cleaned["latency_minutes"] > 360:
        raise ValueError("latency_minutes is implausibly high")
    return cleaned


def validate_caffeine_payload(data: dict) -> dict:
    return {
        "event_date": parse_date(data.get("event_date"), "event_date"),
        "time": validate_time(data.get("time"), "time"),
        "amount_mg": non_negative_number(data.get("amount_mg"), "amount_mg"),
        "beverage_type": (data.get("beverage_type") or "Other").strip()[:60],
    }


def validate_exercise_payload(data: dict) -> dict:
    intensity = str(data.get("intensity", "")).title()
    if intensity not in VALID_INTENSITIES:
        raise ValueError("intensity must be Low, Moderate, or High")
    return {
        "event_date": parse_date(data.get("event_date"), "event_date"),
        "time": validate_time(data.get("time"), "time"),
        "duration_minutes": non_negative_int(data.get("duration_minutes"), "duration_minutes"),
        "intensity": intensity,
    }


def validate_screen_payload(data: dict) -> dict:
    total = non_negative_int(data.get("total_minutes"), "total_minutes")
    pre = non_negative_int(data.get("pre_bed_minutes"), "pre_bed_minutes")
    if pre > total:
        raise ValueError("pre_bed_minutes cannot exceed total_minutes")
    return {
        "event_date": parse_date(data.get("event_date"), "event_date"),
        "total_minutes": total,
        "pre_bed_minutes": pre,
    }


def validate_goal_payload(data: dict) -> dict:
    goal_type = str(data.get("goal_type", ""))
    if goal_type not in VALID_GOAL_TYPES:
        raise ValueError(f"goal_type must be one of: {', '.join(sorted(VALID_GOAL_TYPES))}")
    title = str(data.get("title", "")).strip()
    if not title:
        raise ValueError("title is required")
    target_nights = non_negative_int(data.get("target_nights_per_week", 5), "target_nights_per_week")
    if not 1 <= target_nights <= 7:
        raise ValueError("target_nights_per_week must be between 1 and 7")

    cleaned = {
        "goal_type": goal_type,
        "title": title[:120],
        "target_value": None,
        "target_time": None,
        "target_nights_per_week": target_nights,
        "start_date": parse_date(data.get("start_date"), "start_date"),
        "end_date": parse_date(data["end_date"], "end_date") if data.get("end_date") else None,
        "active": bool(data.get("active", True)),
        "adaptive_enabled": bool(data.get("adaptive_enabled", False)),
    }
    if goal_type == "bedtime_before":
        cleaned["target_time"] = validate_time(data.get("target_time"), "target_time")
    else:
        cleaned["target_value"] = non_negative_number(data.get("target_value"), "target_value")
    if cleaned["end_date"] and cleaned["end_date"] < cleaned["start_date"]:
        raise ValueError("end_date cannot be before start_date")
    return cleaned

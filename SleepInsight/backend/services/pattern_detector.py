from __future__ import annotations

from statistics import mean


def _severity_ratio(value: float, threshold: float, cap_multiplier: float = 2.0) -> float:
    if threshold <= 0:
        return 0.0
    return max(0.0, min(1.0, (value - threshold) / (threshold * (cap_multiplier - 1)) + 0.5))


def detect_patterns(rows: list[dict], analytics: dict) -> list[dict]:
    if not rows:
        return []

    patterns = []
    recent = sorted(rows, key=lambda r: r["sleep_date"])[-7:]

    trend = analytics["trends"]["sleep_duration_7d"]
    if trend["change"] is not None and trend["change"] <= -30:
        patterns.append({
            "rule_id": "declining_sleep_duration",
            "severity": min(1.0, abs(trend["change"]) / 90),
            "title": "Sleep duration is declining",
            "reason": f"Your latest 7-day average is {abs(trend['change']):.0f} minutes lower than the previous 7-day period.",
            "evidence": {"change_minutes": trend["change"], "sample_size": trend["sample_size"]},
            "confidence": "moderate",
        })

    reg = analytics["regularity"]
    if reg["bedtime_sd"] is not None and reg["bedtime_sd"] >= 60:
        patterns.append({
            "rule_id": "inconsistent_sleep_timing",
            "severity": min(1.0, reg["bedtime_sd"] / 120),
            "title": "Bedtime is inconsistent",
            "reason": f"Bedtime variability is {reg['bedtime_sd']:.0f} minutes over the recent analysis window.",
            "evidence": reg,
            "confidence": "moderate" if reg["sample_size"] >= 7 else "low",
        })

    social = analytics["weekday_weekend"].get("social_jetlag_minutes")
    if social is not None and social >= 60:
        patterns.append({
            "rule_id": "weekend_shift",
            "severity": min(1.0, social / 180),
            "title": "Weekend sleep timing shifts substantially",
            "reason": f"Weekday and weekend sleep midpoints differ by about {social:.0f} minutes.",
            "evidence": {"social_jetlag_minutes": social},
            "confidence": "moderate",
        })

    avg_latency = mean(r["latency_minutes"] for r in recent)
    if avg_latency >= 30:
        patterns.append({
            "rule_id": "high_sleep_latency",
            "severity": min(1.0, avg_latency / 60),
            "title": "Sleep latency is elevated",
            "reason": f"Average sleep latency over the last {len(recent)} nights is {avg_latency:.0f} minutes.",
            "evidence": {"average_latency_minutes": round(avg_latency, 1), "sample_size": len(recent)},
            "confidence": "moderate" if len(recent) >= 7 else "low",
        })

    screens = [r["pre_bed_screen_minutes"] for r in recent if r.get("pre_bed_screen_minutes") is not None]
    if screens and mean(screens) >= 60:
        avg_screen = mean(screens)
        patterns.append({
            "rule_id": "high_prebed_screen",
            "severity": min(1.0, avg_screen / 120),
            "title": "Pre-bed screen use is high",
            "reason": f"Average pre-bed screen use is {avg_screen:.0f} minutes across {len(screens)} recent records.",
            "evidence": {"average_prebed_screen_minutes": round(avg_screen, 1), "sample_size": len(screens)},
            "confidence": "moderate" if len(screens) >= 7 else "low",
        })

    late_days = sum(1 for r in recent if r.get("late_caffeine_mg", 0) > 0)
    if late_days >= 3:
        patterns.append({
            "rule_id": "repeated_late_caffeine",
            "severity": min(1.0, late_days / 7),
            "title": "Late caffeine appears repeatedly",
            "reason": f"Late caffeine was recorded on {late_days} of the last {len(recent)} tracked days.",
            "evidence": {"late_caffeine_days": late_days, "sample_size": len(recent)},
            "confidence": "moderate" if len(recent) >= 7 else "low",
        })

    return patterns

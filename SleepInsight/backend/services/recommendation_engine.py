from __future__ import annotations


CONFIDENCE_WEIGHT = {
    "insufficient": 0.0,
    "low": 0.55,
    "moderate": 0.8,
    "high": 1.0,
}

RULE_TEXT = {
    "declining_sleep_duration": "Protect a more consistent sleep opportunity this week and review what changed in your evening routine.",
    "inconsistent_sleep_timing": "Aim for a narrower bedtime window on most nights.",
    "weekend_shift": "Try to reduce the difference between weekday and weekend sleep timing.",
    "high_sleep_latency": "Review the final hour before bed and reduce stimulating activities that may delay sleep onset.",
    "high_prebed_screen": "Reduce screen use during the final hour before bed and compare the next two weeks with your current baseline.",
    "repeated_late_caffeine": "Move caffeine earlier in the day and compare sleep latency with your existing pattern.",
}

GOAL_MATCH = {
    "minimum_sleep_minutes": {"declining_sleep_duration"},
    "bedtime_before": {"inconsistent_sleep_timing", "weekend_shift"},
    "prebed_screen_max": {"high_prebed_screen"},
    "max_sleep_latency": {"high_sleep_latency", "repeated_late_caffeine"},
}


def _correlation_evidence(rule_id: str, correlations: list[dict]) -> tuple[float, str | None]:
    preferred = []
    if rule_id == "high_prebed_screen":
        preferred = [c for c in correlations if c["x"] == "pre_bed_screen_minutes" and c["y"] in {"quality", "duration_minutes"}]
    elif rule_id == "repeated_late_caffeine":
        preferred = [c for c in correlations if c["x"] == "late_caffeine_mg" and c["y"] == "latency_minutes"]

    usable = [c for c in preferred if c.get("rho") is not None and c.get("confidence") != "insufficient"]
    if not usable:
        return 0.65, None
    best = max(usable, key=lambda c: abs(c["rho"]))
    return max(0.5, abs(best["rho"])), f"{best['label']}: ρ={best['rho']:.2f}, n={best['sample_size']}"


def generate_recommendations(patterns: list[dict], correlations: list[dict], goals: list[dict]) -> list[dict]:
    recs = []
    for pattern in patterns:
        evidence_strength, corr_note = _correlation_evidence(pattern["rule_id"], correlations)
        confidence = pattern.get("confidence", "low")
        confidence_weight = CONFIDENCE_WEIGHT.get(confidence, 0.55)

        goal_relevance = 1.0
        for goal in goals:
            if not goal.get("active", True):
                continue
            matches = GOAL_MATCH.get(goal["goal_type"], set())
            if pattern["rule_id"] in matches:
                goal_relevance = 1.2
                break

        priority = min(1.0, pattern["severity"] * evidence_strength * confidence_weight * goal_relevance)
        explanation = pattern["reason"]
        if corr_note:
            explanation += f" Supporting association: {corr_note}."

        recs.append({
            "rule_id": pattern["rule_id"],
            "title": pattern["title"],
            "action": RULE_TEXT.get(pattern["rule_id"], "Review this pattern and test a small behaviour change."),
            "priority_score": round(priority, 3),
            "confidence": confidence,
            "reason": explanation,
            "evidence": pattern.get("evidence", {}),
        })

    return sorted(recs, key=lambda r: r["priority_score"], reverse=True)

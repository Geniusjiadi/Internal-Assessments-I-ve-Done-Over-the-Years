from flask import Blueprint, jsonify, request

from backend.repositories import list_goals
from backend.services.analytics_service import build_analytics, trend_series
from backend.services.pattern_detector import detect_patterns
from backend.services.recommendation_engine import generate_recommendations
from backend.services.goal_engine import goal_progress, adaptive_goal_suggestion
from .common import db_session, load_daily_rows

bp = Blueprint("analytics", __name__, url_prefix="/api")


@bp.get("/analytics/insights")
def insights():
    rows = load_daily_rows()
    analytics = build_analytics(rows)
    analytics["patterns"] = detect_patterns(rows, analytics)
    return jsonify(analytics)


@bp.get("/analytics/trends")
def trends():
    try:
        days = int(request.args.get("days", 30))
    except ValueError:
        days = 30
    days = 7 if days <= 7 else 30 if days <= 30 else 90
    rows = load_daily_rows()
    return jsonify({"days": days, "series": trend_series(rows, days)})


@bp.get("/recommendations")
def recommendations():
    rows = load_daily_rows()
    analytics = build_analytics(rows)
    patterns = detect_patterns(rows, analytics)
    goals = list_goals(db_session())
    recs = generate_recommendations(patterns, analytics["correlations"], goals)
    return jsonify(recs)


@bp.get("/dashboard")
def dashboard():
    rows = load_daily_rows()
    analytics = build_analytics(rows)
    patterns = detect_patterns(rows, analytics)
    goals = list_goals(db_session())
    recs = generate_recommendations(patterns, analytics["correlations"], goals)

    goal_summaries = []
    for goal in goals:
        progress = goal_progress(goal, rows)
        goal_summaries.append({
            **goal,
            "progress": progress,
            "adaptive_suggestion": adaptive_goal_suggestion(goal, progress),
        })

    latest = rows[-1] if rows else None
    return jsonify({
        "record_count": len(rows),
        "latest": latest,
        "sleep_score": analytics["latest_sleep_score"],
        "top_recommendation": recs[0] if recs else None,
        "regularity": analytics["regularity"],
        "sleep_duration_7d": analytics["trends"]["sleep_duration_7d"],
        "goals": goal_summaries[:3],
    })

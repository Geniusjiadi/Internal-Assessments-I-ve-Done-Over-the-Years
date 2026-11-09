from flask import Blueprint, jsonify, request

from backend.repositories import list_goals, create_goal, get_goal, update_goal
from backend.validators import validate_goal_payload
from backend.services.goal_engine import goal_progress, adaptive_goal_suggestion
from .common import db_session, load_daily_rows

bp = Blueprint("goals", __name__, url_prefix="/api/goals")


@bp.get("")
def goals():
    rows = load_daily_rows()
    result = []
    for goal in list_goals(db_session()):
        progress = goal_progress(goal, rows)
        result.append({
            **goal,
            "progress": progress,
            "adaptive_suggestion": adaptive_goal_suggestion(goal, progress),
        })
    return jsonify(result)


@bp.post("")
def add_goal():
    try:
        return jsonify(create_goal(db_session(), validate_goal_payload(request.get_json(silent=True) or {}))), 201
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@bp.put("/<int:goal_id>")
def edit_goal(goal_id):
    item = get_goal(db_session(), goal_id)
    if item is None:
        return jsonify({"error": "Goal not found"}), 404
    try:
        return jsonify(update_goal(db_session(), item, validate_goal_payload(request.get_json(silent=True) or {})))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@bp.delete("/<int:goal_id>")
def remove_goal(goal_id):
    item = get_goal(db_session(), goal_id)
    if item is None:
        return jsonify({"error": "Goal not found"}), 404
    db_session().delete(item)
    return jsonify({"status": "deleted"})

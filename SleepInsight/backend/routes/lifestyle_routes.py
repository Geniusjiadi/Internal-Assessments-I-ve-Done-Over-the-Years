from flask import Blueprint, jsonify, request

from backend.repositories import (
    list_caffeine, create_caffeine,
    list_exercise, create_exercise,
    list_screen, upsert_screen,
)
from backend.validators import validate_caffeine_payload, validate_exercise_payload, validate_screen_payload
from .common import db_session

bp = Blueprint("lifestyle", __name__, url_prefix="/api")


@bp.route("/caffeine", methods=["GET", "POST"])
def caffeine():
    if request.method == "GET":
        return jsonify(list_caffeine(db_session()))
    try:
        return jsonify(create_caffeine(db_session(), validate_caffeine_payload(request.get_json(silent=True) or {}))), 201
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@bp.route("/exercise", methods=["GET", "POST"])
def exercise():
    if request.method == "GET":
        return jsonify(list_exercise(db_session()))
    try:
        return jsonify(create_exercise(db_session(), validate_exercise_payload(request.get_json(silent=True) or {}))), 201
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@bp.route("/screen", methods=["GET", "POST"])
def screen():
    if request.method == "GET":
        return jsonify(list_screen(db_session()))
    try:
        return jsonify(upsert_screen(db_session(), validate_screen_payload(request.get_json(silent=True) or {}))), 201
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

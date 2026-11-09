from flask import Blueprint, jsonify, request
from sqlalchemy import select

from backend.models import SleepRecord
from backend.repositories import list_sleep, create_sleep, update_sleep, delete_sleep
from backend.validators import validate_sleep_payload
from .common import db_session

bp = Blueprint("sleep", __name__, url_prefix="/api/sleep")


@bp.get("")
def get_sleep_records():
    return jsonify(list_sleep(db_session()))


@bp.post("")
def add_sleep_record():
    try:
        data = validate_sleep_payload(request.get_json(silent=True) or {})
        created = create_sleep(db_session(), data)
        return jsonify(created), 201
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@bp.put("/<int:record_id>")
def edit_sleep_record(record_id):
    item = db_session().get(SleepRecord, record_id)
    if item is None:
        return jsonify({"error": "Sleep record not found"}), 404
    try:
        data = validate_sleep_payload(request.get_json(silent=True) or {})
        return jsonify(update_sleep(db_session(), item, data))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@bp.delete("/<int:record_id>")
def remove_sleep_record(record_id):
    item = db_session().get(SleepRecord, record_id)
    if item is None:
        return jsonify({"error": "Sleep record not found"}), 404
    delete_sleep(db_session(), item)
    return jsonify({"status": "deleted"})
